import { existsSync, readFileSync } from 'node:fs';

let failures = 0;
const fail = (msg) => { console.error('  x ' + msg); failures++; };
const ok = (msg) => console.log('  ok ' + msg);

const FILE = 'db/community_events.json';
if (!existsSync(FILE)) {
  fail(FILE + ' is missing');
} else {
  try {
    const raw = JSON.parse(readFileSync(FILE, 'utf8'));
    if (!Array.isArray(raw.events) || raw.events.length === 0) {
      fail('events[] must be a non-empty array');
    } else {
      raw.events.forEach((ev, i) => {
        ['title', 'date', 'mode', 'summary', 'ctaLabel', 'ctaHref'].forEach((k) => {
          if (!ev[k] || typeof ev[k] !== 'string') fail('events[' + i + '].' + k + ' must be a non-empty string');
        });

        if (ev.date && !/^\d{4}-\d{2}-\d{2}$/.test(ev.date)) {
          fail('events[' + i + '].date must be YYYY-MM-DD');
        }

        if (ev.ctaHref) {
          if (ev.ctaHref.startsWith('http://') || ev.ctaHref.startsWith('https://')) {
            try { new URL(ev.ctaHref); } catch { fail('events[' + i + '] has invalid URL: ' + ev.ctaHref); }
          } else {
            const localPath = ev.ctaHref.split('?')[0];
            if (!existsSync(localPath)) fail('events[' + i + '] local target missing: ' + localPath);
          }
        }
      });
    }

    if (!failures) ok(FILE + ' schema checks passed');
  } catch (err) {
    fail(FILE + ' parse error: ' + err.message);
  }
}

if (failures) {
  console.error('\n' + failures + ' community-events validation error(s).');
  process.exit(1);
}
