// Captures the SMIL animation frame by frame (same recipe as plug's docs/scripts/render-diagram.mjs).
//   node render.mjs meerkat-cluster.svg .frames [width height]
// With a width and height (e.g. 1270 760 for Product Hunt), the square scene is centred
// and its background widened to that format.
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const [svg, out, w = '900', h = '900'] = process.argv.slice(2);
const [WIDTH, HEIGHT] = [Number(w), Number(h)];
const DUR = 19; // loop length, seconds (make-svg.py)
const FPS = 12;

mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
await page.goto('file://' + resolve(svg));
await page.evaluate(([w, h]) => {
  const svg = document.documentElement;
  const vw = 900 * w / h, ox = (vw - 900) / 2;
  svg.setAttribute('width', w); svg.setAttribute('height', h);
  svg.setAttribute('viewBox', `${-ox} 0 ${vw} 900`);
  for (const r of svg.querySelectorAll('rect[width="900"][height="900"]')) { r.setAttribute('x', -ox); r.setAttribute('width', vw); }
  svg.pauseAnimations();
}, [WIDTH, HEIGHT]);
for (let i = 0; i < DUR * FPS; i++) {
  await page.evaluate((t) => document.documentElement.setCurrentTime(t), i / FPS);
  await page.screenshot({ path: `${out}/f${String(i).padStart(3, '0')}.png` });
}
await browser.close();
