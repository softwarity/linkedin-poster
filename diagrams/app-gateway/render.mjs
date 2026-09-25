// Captures the SMIL animation frame by frame (same recipe as plug's docs/scripts/render-diagram.mjs).
//   node render.mjs app-gateway.fr.svg frames-fr
import { chromium } from 'playwright';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';

const [svg, out] = process.argv.slice(2);
const DUR = 16; // loop length, seconds (make-svg.py)
const FPS = 12;

mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 900, height: 511 }, deviceScaleFactor: 1 });
await page.goto('file://' + resolve(svg));
await page.evaluate(() => document.documentElement.pauseAnimations());
for (let i = 0; i < DUR * FPS; i++) {
  await page.evaluate((t) => document.documentElement.setCurrentTime(t), i / FPS);
  await page.screenshot({ path: `${out}/f${String(i).padStart(3, '0')}.png` });
}
await browser.close();
