// Drives headless Chrome via raw CDP (no puppeteer dependency) to export a
// reveal.js deck to PDF, waiting for reveal's own `pdf-ready` event before
// printing so every slide is captured — not just the first page.
//
// Requires Node 18+ (native fetch) — actually Node 21+ for native
// WebSocket. Requires a Chrome instance already running with
// --remote-debugging-port reachable at http://localhost:<port>.
//
// Usage: node print_pdf.js <fileOrHttpUrl> <outPath> [cdpPort=9333]
const fs = require('fs');

const [,, targetUrl, outPath, portArg] = process.argv;
if (!targetUrl || !outPath) {
  console.error('usage: node print_pdf.js <url> <outPath> [cdpPort=9333]');
  process.exit(1);
}
const port = portArg || 9333;

async function main() {
  const newTabRes = await fetch(`http://localhost:${port}/json/new?about:blank`, { method: 'PUT' });
  const tab = await newTabRes.json();
  const ws = new WebSocket(tab.webSocketDebuggerUrl);

  let id = 0;
  const pending = new Map();
  const eventWaiters = [];

  function send(method, params = {}) {
    const thisId = ++id;
    return new Promise((resolve, reject) => {
      pending.set(thisId, { resolve, reject });
      ws.send(JSON.stringify({ id: thisId, method, params }));
    });
  }

  function waitForConsoleMarker(marker, timeoutMs) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(() => reject(new Error('timeout waiting for ' + marker)), timeoutMs);
      eventWaiters.push({ marker, resolve: () => { clearTimeout(timer); resolve(); } });
    });
  }

  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve);
    ws.addEventListener('error', reject);
  });

  ws.addEventListener('message', (ev) => {
    const msg = JSON.parse(ev.data);
    if (msg.id && pending.has(msg.id)) {
      const { resolve, reject } = pending.get(msg.id);
      pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
    if (msg.method === 'Runtime.consoleAPICalled') {
      const text = (msg.params.args || []).map(a => a.value).join(' ');
      for (let i = eventWaiters.length - 1; i >= 0; i--) {
        if (text.includes(eventWaiters[i].marker)) {
          eventWaiters[i].resolve();
          eventWaiters.splice(i, 1);
        }
      }
    }
  });

  await send('Page.enable');
  await send('Runtime.enable');

  // Inject a listener for reveal's 'pdf-ready' event BEFORE navigation, via
  // Page.addScriptToEvaluateOnNewDocument so it's present at load time.
  // Reveal only dispatches this once every slide has been laid out into its
  // own .pdf-page div — a raw --print-to-pdf CLI print fires before that
  // finishes and only captures whatever partial DOM exists (usually just
  // page 1).
  await send('Page.addScriptToEvaluateOnNewDocument', {
    source: `
      window.__pdfReady = false;
      document.addEventListener('DOMContentLoaded', function () {
        var tries = 0;
        var iv = setInterval(function () {
          tries++;
          if (window.Reveal && typeof window.Reveal.on === 'function') {
            clearInterval(iv);
            window.Reveal.on('pdf-ready', function () {
              window.__pdfReady = true;
              console.log('__PDF_READY__');
            });
          } else if (tries > 200) {
            clearInterval(iv);
          }
        }, 25);
      });
    `
  });

  await send('Page.navigate', { url: targetUrl });
  await new Promise((resolve) => {
    const handler = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.method === 'Page.loadEventFired') {
        ws.removeEventListener('message', handler);
        resolve();
      }
    };
    ws.addEventListener('message', handler);
  });

  try {
    await waitForConsoleMarker('__PDF_READY__', 30000);
  } catch (e) {
    console.error('WARNING:', e.message, '-- printing anyway after fallback delay');
    await new Promise(r => setTimeout(r, 5000));
  }

  // Give layout one more paint cycle to settle.
  await new Promise(r => setTimeout(r, 500));

  const result = await send('Page.printToPDF', {
    printBackground: true,
    preferCSSPageSize: true,
    marginTop: 0,
    marginBottom: 0,
    marginLeft: 0,
    marginRight: 0,
  });

  fs.writeFileSync(outPath, Buffer.from(result.data, 'base64'));
  console.log('wrote', outPath);

  await send('Page.close').catch(() => {});
  ws.close();
}

main().catch((e) => { console.error(e); process.exit(1); });
