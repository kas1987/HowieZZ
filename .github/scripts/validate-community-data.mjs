import { existsSync, readFileSync } from 'node:fs';

let failures = 0;
const fail = (msg) => { console.error('  x ' + msg); failures++; };
const ok = (msg) => console.log('  ok ' + msg);

const FILE = 'db/community_channels.json';
if (!existsSync(FILE)) {
  fail(FILE + ' is missing');
} else {
  try {
    const raw = JSON.parse(readFileSync(FILE, 'utf8'));

    if (!raw.meta || typeof raw.meta !== 'object') fail('meta object is missing');
    if (!Array.isArray(raw.channels) || raw.channels.length === 0) fail('channels[] must be non-empty');
    if (!Array.isArray(raw.official_handles)) fail('official_handles[] must be present');

    const refs = raw.meta && Array.isArray(raw.meta.source_refs) ? raw.meta.source_refs : [];
    if (!refs.length) fail('meta.source_refs[] must include at least one provenance entry');

    refs.forEach((r, i) => {
      if (!r || typeof r !== 'object') {
        fail('source_refs[' + i + '] invalid');
        return;
      }
      if (!r.path || !r.kind) fail('source_refs[' + i + '] must include path and kind');
      if (r.path && !existsSync(r.path)) fail('source_refs[' + i + '] path missing: ' + r.path);
    });

    const requiredChannelFields = ['name', 'purpose', 'status', 'cadence', 'primary', 'secondary', 'primaryLabel', 'secondaryLabel'];
    raw.channels.forEach((c, i) => {
      requiredChannelFields.forEach((k) => {
        if (!c[k] || typeof c[k] !== 'string') fail('channels[' + i + '].' + k + ' must be a non-empty string');
      });
      [c.primary, c.secondary].forEach((u) => {
        if (!u) return;
        if (u.startsWith('http://') || u.startsWith('https://')) {
          try { new URL(u); } catch { fail('channels[' + i + '] has invalid URL: ' + u); }
        } else {
          const localPath = u.split('?')[0];
          if (!existsSync(localPath)) fail('channels[' + i + '] local target missing: ' + localPath);
        }
      });
    });

    const requiredHandleFields = ['platform', 'handle', 'url', 'verification'];
    raw.official_handles.forEach((h, i) => {
      requiredHandleFields.forEach((k) => {
        if (!h[k] || typeof h[k] !== 'string') fail('official_handles[' + i + '].' + k + ' must be a non-empty string');
      });
      const p = (h.url || '').split('?')[0];
      if (p && !(h.url.startsWith('http://') || h.url.startsWith('https://')) && !existsSync(p)) {
        fail('official_handles[' + i + '] local target missing: ' + p);
      }
    });

    if (!failures) ok(FILE + ' schema and provenance checks passed');
  } catch (err) {
    fail(FILE + ' parse error: ' + err.message);
  }
}

if (failures) {
  console.error('\n' + failures + ' community data validation error(s).');
  process.exit(1);
}
