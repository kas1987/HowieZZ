# Documentation Index & Quick Start Guide

**ZELEX Character Atlas** — Complete Documentation Suite

All 6 comprehensive reference documents are now available in the root directory.

---

## Start Here

### **New to the project?** → Read [ARCHITECTURE.md](ARCHITECTURE.md) first

**[ARCHITECTURE.md](ARCHITECTURE.md)** (662 lines) is your entry point. It covers:
- What ZELEX is (at a glance)
- How it works (data flow diagram)
- Technology stack
- Key design principles
- Page routing & features
- Where everything lives (repository structure)

**Time investment:** 15–20 minutes → full mental model of the system

---

## By Role

### I'm a **Developer** (building features, fixing bugs)

**Path:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) — System overview & constraints
2. [API.md](API.md) — Runtime API reference (ZX global object)
3. [DATA-SCHEMA.md](DATA-SCHEMA.md) — Data structures you'll work with
4. [DECISIONS.md](DECISIONS.md) — Why things are designed this way

**Quick lookup:** [GLOSSARY.md](GLOSSARY.md) for terminology

**Time:** 1–2 hours to full fluency

---

### I'm a **Data / Build Engineer** (running pipelines, managing catalog)

**Path:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) → Section "Build Pipeline"
2. [DATA-SCHEMA.md](DATA-SCHEMA.md) → File-level schemas + validation rules
3. [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → Adding bodies, editing characters
4. `docs/BUILD-ORCHESTRATOR.md` → Detailed pipeline mechanics

**Quick lookup:** [GLOSSARY.md](GLOSSARY.md) (Body, Character, WHR/BWR, etc.)

**Time:** 2–3 hours to operational readiness

---

### I'm a **Product / Content Manager** (personas, stories, positioning)

**Path:**
1. [GLOSSARY.md](GLOSSARY.md) → Understand the terminology
2. [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Adding a New Character" section
3. [DATA-SCHEMA.md](DATA-SCHEMA.md) → `character_overlay.json` schema
4. `docs/story-schema.md` → Story writing guidelines

**No need to read:** API.md (unless curious about runtime)

**Time:** 1 hour to start contributing

---

### I'm an **Operations / DevOps** (deployments, monitoring, incidents)

**Path:**
1. [ARCHITECTURE.md](ARCHITECTURE.md) → "Deployment" section
2. [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → All sections (deployment, rollback, troubleshooting)
3. `docs/BUILD-ORCHESTRATOR.md` → Pipeline exit codes & state tracking
4. [README.md](README.md) → Quick build commands

**Critical:** [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) "Troubleshooting" section

**Time:** 1–1.5 hours to operational readiness

---

## By Task

### "I need to add a new body to the catalog"

→ [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Adding a New Body"

**Steps:** 8 steps, ~20 minutes
- Create spec card image
- Add measurements to JSON
- Run build pipeline
- Verify classification
- Link photoshoots
- Generate characters
- Curate personas (optional)
- Deploy via git PR

---

### "I need to fix a character's name or story"

→ [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Editing Existing Characters"

**Steps:** Edit JSON overlay → Re-run build → Deploy

**Time:** 5 minutes

---

### "The site is down or behaving oddly"

→ [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Troubleshooting"

**7 common issues covered:**
- Build fails with input hash mismatch
- Character not appearing
- WHR/BWR out of range
- Images not loading
- Analytics not tracking

---

### "I'm deploying changes to production"

→ [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Deploying Changes"

**Pre-deployment checklist** (8 items)
**Deployment steps** (7 steps)
**Rollback procedure** (if something goes wrong)

---

## Document Map

| Document | Length | Purpose | Best For |
|----------|--------|---------|----------|
| **[ARCHITECTURE.md](ARCHITECTURE.md)** | 662 lines | System design overview | Entry point, new team members |
| **[DATA-SCHEMA.md](DATA-SCHEMA.md)** | 866 lines | Detailed schema specs | Data engineers, implementers |
| **[API.md](API.md)** | 883 lines | Runtime API reference | Frontend developers, integrations |
| **[GLOSSARY.md](GLOSSARY.md)** | 539 lines | Terminology index | Everyone (bookmark for quick lookup) |
| **[DECISIONS.md](DECISIONS.md)** | 694 lines | Architecture decisions | Architects, design reviews |
| **[MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)** | 657 lines | Operational procedures | Product, content, DevOps teams |

**Total:** 4,301 lines of documentation (~120 KB)

---

## Common Questions Answered

**Q: Where's the API documentation?**
A: [API.md](API.md) — All 40+ methods of the ZX global object.

**Q: What are the 6 Body Families?**
A: [GLOSSARY.md](GLOSSARY.md) → "Body Family" + [ARCHITECTURE.md](ARCHITECTURE.md) → "Core Domains" section.

**Q: How do I add a new body?**
A: [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Adding a New Body" (8 steps).

**Q: Why no framework or build step?**
A: [DECISIONS.md](DECISIONS.md) → "No Framework, No Build Step" (with full rationale).

**Q: What's WHR and BWR?**
A: [GLOSSARY.md](GLOSSARY.md) → "WHR (Waist-Hip Ratio)" + "BWR (Bust-Waist Ratio)".

**Q: How does the build pipeline work?**
A: [ARCHITECTURE.md](ARCHITECTURE.md) → "Build Pipeline" + [DATA-SCHEMA.md](DATA-SCHEMA.md) → "Build State & Metadata".

**Q: How do I deploy changes?**
A: [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Deploying Changes" (with checklist).

**Q: What if something breaks?**
A: [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → "Troubleshooting" (7 scenarios) or "Rolling Back".

---

## Bookmarks (Save These)

- **Daily reference:** [GLOSSARY.md](GLOSSARY.md)
- **Build issues:** [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md) → Troubleshooting
- **API lookup:** [API.md](API.md)
- **Schema questions:** [DATA-SCHEMA.md](DATA-SCHEMA.md)
- **"Why did we design it this way?"** [DECISIONS.md](DECISIONS.md)
- **"How do I…?"** [MIGRATION-GUIDE.md](MIGRATION-GUIDE.md)

---

## Before You Start

✓ Read [ARCHITECTURE.md](ARCHITECTURE.md) (15–20 min)
✓ Bookmark [GLOSSARY.md](GLOSSARY.md)
✓ Skim your role's section above
✓ Keep [README.md](README.md) handy for quick commands

---

## Maintenance & Updates

These docs are versioned with the codebase. If you make changes:

1. **Update the relevant doc** (ARCHITECTURE.md, DATA-SCHEMA.md, API.md, etc.)
2. **Update cross-references** (other docs may link to changed sections)
3. **Update GLOSSARY.md** if terminology changes
4. **Update DECISIONS.md** if a major design decision changes
5. **Commit together** with code changes (same PR/commit)

**Rule:** No code change without doc update.

---

## Questions?

If documentation is unclear or incomplete:
- File an issue or PR with suggestions
- Update the doc yourself (you have permission)
- Ask on Slack / team channel

Documentation is a living reference; improvements are always welcome.

---

**Last updated:** 2026-06-21
**Status:** Complete coverage of architecture, data structures, API, operations, and terminology
**Ready for:** Onboarding, architecture review, reference lookups, operational handoff
