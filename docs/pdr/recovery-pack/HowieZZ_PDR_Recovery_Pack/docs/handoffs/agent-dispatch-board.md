# Agent Dispatch Board

| Task ID | Agent | Mission | Source files | Evidence required | Acceptance criteria | Stop condition | Priority | Status |
|---|---|---|---|---|---|---|---:|---|
| HZZ-P0-001 | Archivist | Add PDR recovery package to HowieZZ | docs/pdr/* | PR diff shows files in HowieZZ | All PDRs present under docs/pdr | If repo target is not HowieZZ | P0 | ready |
| HZZ-P0-002 | Chainbreaker | Confirm GitHub connector/write routing | GitHub connector logs | `get_repo` resolves HowieZZ correctly | No writes to wrong repo | If write target resolves Command-Center/3D_Meta | P0 | blocked |
| HZZ-P1-001 | Cartographer | Implement homepage concierge modules | index.html, site.css | Screenshots desktop/mobile | Trust strip/family chooser/compare/concierge blocks render | If images/data unavailable breaks page | P1 | ready |
| HZZ-P1-002 | Cartographer | Implement body compare scaffold | compare.html, site.js, site.css | Local static test | Compare 2-4 bodies and contact handoff | If db shape differs from expected | P1 | ready |
| HZZ-P1-003 | Auditor | Validate no PII analytics leakage | site.js, contact.html | Event payload inspection | No name/email/phone/message in events | If analytics is undefined | P1 | blocked |
| HZZ-P2-001 | Cartographer | Upgrade quiz result funnel | quiz.html, site.js | Saved quiz result and result UI | Top 3 scores + explanation + CTAs | If family coverage is too thin | P2 | ready |
| HZZ-P2-002 | Cartographer | Upgrade character detail conversion | character.html | Character pages test | Buyer-fit notes + compare/contact CTAs | If metadata missing | P2 | ready |
| HZZ-P2-003 | Archivist | Add taxonomy docs and JSON | db/*.json, docs/taxonomy | Family map produced | Every body has status | If measurement data missing | P2 | ready |
| HZZ-P2-004 | Financier | Produce competitor ROI matrix | docs/research/* | Source log + CSV | 80+ profiles or blocker documented | If sources insufficient | P2 | ready |
| HZZ-P3-001 | Sentinel | SEO/metadata generation | scripts/*, docs/* | Generated sitemap/metadata | Validation checklist passes | If URL strategy undecided | P3 | ready |
