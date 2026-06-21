# Operations & Handoff Index

**Brand Team Operational Readiness Package**

This folder contains all documentation needed for the brand team to operate ZELEX Character Atlas in production.

---

## Quick Start (15 minutes)

**New to the team?** Start here:

1. **[QUICK-REFERENCE.md](QUICK-REFERENCE.md)** — Print this wallet card
2. **[SLA-TARGETS.md](SLA-TARGETS.md)** — Understand our commitments (5 min)
3. **[BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md)** — Start training (4 hours, self-paced)

---

## Before Your First On-Call Shift

Complete this checklist:

- [ ] Read [BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md) completely
- [ ] Review [OPERATIONS.md](../OPERATIONS.md) runbooks (focus on top 3 issues)
- [ ] Do hands-on exercises in training guide
- [ ] Set up local environment (`python serve.py`)
- [ ] Print [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- [ ] Get emergency contact list filled in
- [ ] Schedule 30-min walkthrough with previous on-call
- [ ] Confirm you can access GitHub + Slack

**First shift ready?** Slack: `@zelex-ops-oncall I'm ready`

---

## Core Documents

### [OPERATIONS.md](../OPERATIONS.md) ⭐ PRIMARY RUNBOOK

**Use this when responding to incidents.**

- On-call rotation schedule + responsibilities
- Incident severity matrix (P1/P2/P3/P4)
- Escalation paths and emergency contacts
- **7 detailed runbooks** (copy & paste steps):
  - Site Down (P1)
  - CI Build Failure
  - Catalog Corruption
  - Performance Degradation
  - Payment Form Broken
  - Shopify Sync Failed
  - Missing/Wrong Image
- SLA definitions and metrics
- Post-mortem process

**When to use**: Every incident. Bookmark this file.

---

### [BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md) ⭐ TRAINING GUIDE

**Use to learn the system.**

- Part 1: Architecture overview (what is ZELEX?)
- Part 2: Data pipeline (how does data flow?)
- Part 3: Common issues & fixes (30 min)
- Part 4: Monitoring & on-call (45 min)
- Part 5: Hands-on exercises (2 hours)
- Part 6: SLA & expectations
- Part 7: Document index
- Part 8: Knowledge quiz (8 questions)
- Readiness checklist

**How to use**: Self-paced, 6 hours total (including exercises)

**First-timer?** Do this before your first shift.

---

### [MONITORING-CONFIG.md](MONITORING-CONFIG.md)

**How to set up monitoring and alerting.**

- Monitoring services (Uptime Robot, GitHub Actions, custom scripts)
- 7 alert rules (with Slack message templates)
- Step-by-step setup (create account, configure webhooks)
- Custom monitoring scripts (catalog freshness, schema validation)
- Performance dashboard template
- Alert fatigue prevention
- On-call handoff protocol
- Weekly/monthly/quarterly maintenance tasks

**When to use**: First-time setup, quarterly review

**DevOps task**: Follow these steps in the first week.

---

### [POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md)

**How to document incidents.**

- Executive summary
- Impact metrics (users, downtime, revenue)
- Timeline (when did each event happen?)
- Root cause analysis (5-whys)
- Contributing factors checklist
- Lessons learned (what went well? what could be better?)
- Action items (prevent recurrence)
- Communication log (internal + external)
- Appendix (logs, config, references)
- Sign-off (who reviewed?)

**When to use**: After every P1/P2 incident (required), optional for P3

**Due**: Within 24 hours of resolution (P1), 1 week (P2)

---

### [QUICK-REFERENCE.md](QUICK-REFERENCE.md) 📱

**Wallet card — print or save to phone.**

- Incident severity matrix
- Top 5 issues & quick fixes
- Emergency contacts
- Critical commands (git, python, bash)
- Escalation flowchart
- Tool links (GitHub, Slack, Uptime Robot)
- Slack commands
- Git workflow
- Quick health check
- SLA targets
- Runbook index

**When to use**: During incident response (have it open on second monitor or printed)

---

### [SLA-TARGETS.md](SLA-TARGETS.md)

**Our promises to stakeholders.**

- Availability SLA: 99.5% uptime (18 min/month allowed)
- Response SLA: P1 (15 min), P2 (1 hr), P3 (4 hr), P4 (best effort)
- Data freshness: <6 hours old
- Performance: p99 latency <2 seconds
- Build: <10 min, deploy <5 min
- On-call coverage: 24/7 for P1
- Monthly metrics & KPIs
- SLA credits for breaches
- Escalation triggers
- Review & adjustment process

**When to use**: Understand commitments, monthly review, budget decisions

---

## Supporting Materials

### [../OPERATIONS.md](../OPERATIONS.md) (Root Folder)

Main runbook. Linked from other docs.

### [../SECURITY.md](../SECURITY.md)

Security incident procedure (don't post in #zelex-ops, email security@).

### [../SITE-GUIDE.md](../SITE-GUIDE.md)

Site pages, features, data, pipeline. Reference for how the system works.

### [../CLAUDE.md](../CLAUDE.md)

Tech stack, how to run locally, git workflow. Reference for developers.

---

## Typical On-Call Workflow

```
Monday 00:00 UTC → Your shift starts

1. Check dashboard
   - GitHub Actions: https://github.com/kas1987/HowieZZ/actions
   - Uptime Robot: https://uptimerobot.com
   - Slack #zelex-ops bookmark for status

2. Verify site is up
   curl https://www.zelexdoll.com

3. Daily health check (do this each day)
   ☐ Site loads
   ☐ Browse works
   ☐ No red badges in GitHub Actions
   ☐ No Slack alerts (or all resolved)

4. Incident occurs (you see a Slack alert)
   - Read alert message
   - Check severity using matrix
   - Open OPERATIONS.md runbook
   - Follow steps (don't improvise)
   - Document actions in Slack thread
   - Escalate if stuck

5. End of shift (Sunday 23:30 UTC)
   - Brief the next on-call (30 min)
   - Review: open issues, recent incidents
   - Handoff: what to watch for
   - Send summary email: ops@zelexdoll.com

6. Post-mortem (if P1/P2 happened)
   - Use POSTMORTEM-TEMPLATE.md
   - Due within 24 hours (P1) or 1 week (P2)
   - Post in #zelex-ops when complete
```

---

## Escalation Quick Map

```
Problem detected
    ↓
Can I follow a runbook? → YES → Do it
    ↓ NO
Slack: @zelex-ops-oncall "Help with [issue]"
    ↓
Security issue?
    YES → Email: security@zelexdoll.com
    NO → Continue investigation
    ↓
P1 (site down)?
    YES → Also email: lead-engineer@zelexdoll.com, cc: ceo
    NO → P2/P3/P4 standard triage
```

---

## Key Contacts

**Update this section with real names/emails/phones.**

| Role | Name | Email | Phone | Slack |
|---|---|---|---|---|
| **CEO** | Howie Wang | howie@zelexdoll.com | — | @howie |
| **Lead Engineer** | [TO FILL] | [email] | [phone] | @[slack] |
| **DevOps/SRE** | [TO FILL] | [email] | [phone] | @[slack] |
| **On-Call Lead** | [Rotates weekly] | — | [on-call phone] | @zelex-ops-oncall |
| **Security Officer** | — | kas41866@gmail.com | — | — |

---

## Common Tasks

### I'm starting my on-call shift
→ Read [BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md) § Checklist  
→ Print [QUICK-REFERENCE.md](QUICK-REFERENCE.md)  
→ Set up Slack notifications

### I see an incident alert
→ Open [OPERATIONS.md](../OPERATIONS.md) § Incident Triage  
→ Determine severity  
→ Follow the runbook  

### I want to learn about ZELEX
→ Start with [BRAND-TEAM-TRAINING.md](BRAND-TEAM-TRAINING.md)  
→ Do hands-on exercises  
→ Take the quiz

### I need to set up monitoring
→ Follow [MONITORING-CONFIG.md](MONITORING-CONFIG.md) step-by-step  
→ Uptime Robot setup first (5 min)  
→ GitHub integration second (10 min)

### An incident just happened
→ Use [POSTMORTEM-TEMPLATE.md](POSTMORTEM-TEMPLATE.md)  
→ Fill in sections (1–1.5 hours)  
→ Post in #zelex-ops when done

### I want to understand our commitments
→ Read [SLA-TARGETS.md](SLA-TARGETS.md)  
→ Bookmark for reference  
→ Review monthly

### Something feels wrong
→ Check [QUICK-REFERENCE.md](QUICK-REFERENCE.md) § First Steps  
→ Verify status (site up? CI green?)  
→ Ask for help if unsure

---

## Document Maintenance

| Document | Owner | Review Schedule | Last Updated |
|---|---|---|---|
| OPERATIONS.md | On-Call Lead | Monthly | 2026-06-21 |
| BRAND-TEAM-TRAINING.md | Training Lead | Quarterly | 2026-06-21 |
| MONITORING-CONFIG.md | DevOps | Quarterly | 2026-06-21 |
| POSTMORTEM-TEMPLATE.md | SRE Lead | After each incident | 2026-06-21 |
| QUICK-REFERENCE.md | On-Call Lead | Monthly | 2026-06-21 |
| SLA-TARGETS.md | SRE Lead | Quarterly | 2026-06-21 |

**How to contribute**: Submit PR with improvements, tag document owner for review.

---

## Success Metrics

After 1 month of operations, we should see:

- ✓ Zero P1 incidents due to unclear runbooks (all issues documented)
- ✓ All P1/P2 incidents documented in post-mortems within SLA
- ✓ Team completes training & passes quiz 100%
- ✓ Monitoring alerts all tuned (no false positives)
- ✓ On-call handoffs smooth with <5 min escalation on unclear issues
- ✓ Site maintains 99.5% uptime

---

## Getting Help

| Question | Answer | Where |
|---|---|---|
| How do I start my shift? | Readiness checklist | BRAND-TEAM-TRAINING.md |
| What's the SLA? | See table | SLA-TARGETS.md |
| How do I respond to X issue? | Follow runbook | OPERATIONS.md |
| What's the incident severity? | Use matrix | QUICK-REFERENCE.md |
| Who do I contact for Y? | See contacts | This page (top) |
| I'm stuck on Z | Post in Slack | #zelex-ops |

---

## Feedback

Is something unclear or missing?

1. Slack: Post feedback in `#zelex-ops` thread
2. GitHub: Open issue with label `documentation`
3. Email: ops@zelexdoll.com with suggestions

We update docs based on real incidents and team feedback.

---

**Version**: 1.0  
**Effective Date**: 2026-06-21  
**Next Review**: 2026-09-21  
**Status**: Ready for Brand Team Operations

---
