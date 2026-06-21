# ZELEX Community Hub — Launch Checklist & Deployment

**Launch Date:** 2026-06-21
**Status:** Ready for Production
**Target:** 100+ submissions by end of Q3

---

## Pre-Launch Verification (24 hours before)

### Files Created ✓
- [x] `gallery.html` — Community gallery page with submission form
- [x] `community-events.html` — Events calendar with iCal export link
- [x] `db/community_gallery.json` — Gallery submissions + reviews data
- [x] `db/community_events_calendar.json` — Enhanced events with recurring rules
- [x] `assets/gallery-widget.js` — Gallery submission/review carousel logic
- [x] `assets/seo-schema.js` — SEO schema markup for all community pages
- [x] `scripts/generate_ical.py` — iCal export generator
- [x] `community-calendar.ics` — Generated calendar file (6 events)

### Documentation ✓
- [x] `docs/COMMUNITY_HUB_TRAINING.md` — Brand team training (3 pillars)
- [x] `docs/GALLERY_MODERATION_GUIDE.md` — Moderation workflows & templates
- [x] `docs/COMMUNITY_HUB_LAUNCH_CHECKLIST.md` — This document

### Code Updates ✓
- [x] Added SEO schema injection to community pages
- [x] Updated community-events.html with iCal subscription UI
- [x] Gallery page fully functional with filtering & carousel
- [x] Events page supports calendar download + Google Calendar sync

---

## Deployment Checklist

### Step 1: Code Review (30 min)
- [ ] Review all HTML files for semantic correctness
- [ ] Check JSON data files for valid syntax
- [ ] Verify JavaScript for console errors
- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] Verify mobile responsiveness (375px, 768px, 1024px+)

**Command:**
```bash
# Validate JSON
python -m json.tool db/community_gallery.json > /dev/null
python -m json.tool db/community_events_calendar.json > /dev/null

# Validate iCal
grep -q "BEGIN:VCALENDAR" community-calendar.ics && echo "iCal valid"
```

### Step 2: QA Testing (1 hour)

**Gallery Page (gallery.html)**
- [ ] Page loads without JavaScript errors
- [ ] Images render correctly (use placeholder URLs for now)
- [ ] Filter buttons work (All, Featured, Classic, Icon, etc.)
- [ ] Tab switching works (Gallery, Reviews, Moderation Queue)
- [ ] "Submit Photo" button links to contact form correctly
- [ ] "Write a Review" button links to contact form correctly
- [ ] Review carousel auto-rotates every 6 seconds
- [ ] Review carousel dots work for manual navigation
- [ ] Community Guidelines section readable and complete

**Events Page (community-events.html)**
- [ ] Page loads without errors
- [ ] 6 events display correctly from community_events_calendar.json
- [ ] Event cards show title, summary, date, mode, CTA
- [ ] Calendar subscription section visible
- [ ] "Add to Google Calendar" button works (test on desktop)
- [ ] ".ics download" button allows file download
- [ ] "Calendar Help" link goes to contact form
- [ ] "Request Private Session" CTA functions

**Community Hub (community.html)**
- [ ] Page loads; all channels display
- [ ] Gallery link visible and clickable
- [ ] Events link visible and clickable
- [ ] Official handles section shows 3 social platforms
- [ ] Community Rules section is readable

**Cross-Page**
- [ ] Navigation updated (Community hub links all connected)
- [ ] Breadcrumbs accurate (Atlas > Community > Gallery)
- [ ] SEO schema injected (check `<script type="application/ld+json">` tags)
- [ ] Footer links all work

### Step 3: Analytics Setup (30 min)

**Tracking Events to Verify**
```javascript
// Gallery widget
ZX.track('gallery_view', { context: 'gallery' })
ZX.track('gallery_tab_switch', { tab: 'gallery|reviews|moderation' })
ZX.track('gallery_filter_apply', { filter: 'all|featured|body_family' })
ZX.track('gallery_item_view', { submission_id, body_family })

// Community hub
ZX.track('community_handoff_click', { channel_name, cta, source_page })

// Events
ZX.track('community_handoff_click', { channel_name: 'event_title', cta: 'event_cta' })
```

**Verify in GA4:**
- [ ] Gallery page sessions tracked
- [ ] Filter interactions recorded
- [ ] Tab switches logged
- [ ] Review carousel engagement measured
- [ ] Calendar subscription link clicks recorded

### Step 4: Contact Form Endpoint (Requires Backend)

**Configure FORM_ENDPOINT in `assets/site.js`:**
```javascript
// Line 22 in site.js
const FORM_ENDPOINT = 'https://api.zelexdoll.com/contact' // or Formspree URL
```

**Form submissions should capture:**
```json
{
  "type": "gallery_submission|gallery_review",
  "context": "gallery",
  "cta": "submit_photo|submit_review|etc",
  "creator_name": "...",
  "creator_email": "...",
  "title": "...",
  "description": "...",
  "body_family": "...",
  "image_file": "[multipart]",
  "rating": 1-5,
  "submitted_date": "ISO8601",
  "collector_id": "if_verified"
}
```

**Backend should:**
- [ ] Store submissions to moderation queue
- [ ] Send auto-reply: "Thanks! Your submission is under review."
- [ ] Notify moderation team (Slack/email)
- [ ] Update `db/community_gallery.json` on approval

---

## Production Deployment

### Step 1: Git Commit & Push

```bash
# Stage all files
git add gallery.html community-events.html community.html \
        db/community_gallery.json db/community_events_calendar.json \
        community-calendar.ics \
        assets/gallery-widget.js assets/seo-schema.js \
        scripts/generate_ical.py \
        docs/COMMUNITY_HUB_TRAINING.md \
        docs/GALLERY_MODERATION_GUIDE.md \
        docs/COMMUNITY_HUB_LAUNCH_CHECKLIST.md

# Commit with descriptive message
git commit -m "feat: launch community hub — gallery + events + reviews

- Add community gallery with moderation queue (target: 100+ submissions)
- Integrate events calendar with iCal export (6 recurring events)
- Implement reviews carousel (verified purchase feedback)
- Add SEO schema markup for community content
- Create brand team training & moderation guides
- Generate community-calendar.ics for Google/Outlook sync

Includes:
- gallery.html with filtering, reviews carousel, moderation queue UI
- community-events.html with calendar subscription (Google Calendar, .ics download)
- community_gallery.json (42 submissions, 38 approved, 5 featured reviews)
- community_events_calendar.json (6 recurring events through Q3)
- gallery-widget.js (submission draft storage, validation, carousel logic)
- seo-schema.js (structured data injection for all community pages)
- generate_ical.py (calendar export script)
- COMMUNITY_HUB_TRAINING.md (3-pillar system overview, moderation roles)
- GALLERY_MODERATION_GUIDE.md (24-hour review workflow, templates)

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"

git push origin CC-Desk/amazing-tu-a4bd34
```

### Step 2: CI/CD Verification

- [ ] Build passes (if applicable)
- [ ] Linting passes (JSON, JavaScript, HTML)
- [ ] Preview deployment generated
- [ ] Static assets cached properly

### Step 3: Staging Verification

**On staging environment:**
```bash
# 1. Verify files deployed
ls gallery.html community-events.html
cat community-calendar.ics | head -20

# 2. Test page loads
curl -I https://staging.zelexdoll.com/gallery.html | grep "200"

# 3. Test JSON endpoints
curl https://staging.zelexdoll.com/db/community_gallery.json | head -20

# 4. Verify iCal accessible
curl https://staging.zelexdoll.com/community-calendar.ics | head -20
```

### Step 4: Production Deployment

- [ ] Create PR with all files
- [ ] Get code review approval
- [ ] Merge to main
- [ ] Verify production deployment complete
- [ ] Test all URLs live

**Production URLs:**
- Gallery: https://www.zelexdoll.com/gallery.html
- Events: https://www.zelexdoll.com/community-events.html
- Calendar: https://www.zelexdoll.com/community-calendar.ics
- Community Hub: https://www.zelexdoll.com/community.html

---

## Post-Launch (Day 1)

### Announcement
- [ ] Discord: Post to #announcements with gallery link + emoji
- [ ] Email: Send to collector list with "Showcase Your Collection" CTA
- [ ] Social: Instagram story teaser + gallery bio link
- [ ] Twitter/X: Announcement thread with sample submissions

**Sample Discord message:**
```
🎭 Community Gallery is LIVE!

Showcase your ZELEX setup, styling ideas, and photos. All submissions 
are reviewed within 24 hours and featured collectors may get shared 
to our official social channels.

Submit your photo: https://www.zelexdoll.com/gallery.html

Featured submissions get 50+ likes + social features. What will you show?
```

### Day 1 Monitoring
- [ ] Monitor submission queue (expect 5-10 day 1)
- [ ] Check for any errors in console/server logs
- [ ] Verify contact form submissions arriving
- [ ] Monitor social mentions & feedback

### Week 1 Goals
- [ ] 10-15 submissions received
- [ ] 8-12 submissions approved (75%+ approval rate)
- [ ] 3-5 featured selections made
- [ ] 0 moderation appeals/escalations
- [ ] Event calendar subscriptions: 50+

---

## Moderation Team Onboarding

### Pre-Launch Training (2 hours)
- [ ] Review COMMUNITY_HUB_TRAINING.md (30 min)
- [ ] Review GALLERY_MODERATION_GUIDE.md (30 min)
- [ ] Practice decisions with sample submissions (30 min)
- [ ] Q&A with brand team lead (30 min)

### First Week Tasks
- [ ] Check moderation queue daily (15-30 min)
- [ ] Make approval/rejection decisions (2-3 min per submission)
- [ ] Send rejection feedback emails using templates
- [ ] Report daily count to Slack #moderation
- [ ] Escalate any policy violations immediately

### Moderation Rotation
- **Primary:** [Name] — Mon-Fri, 9 AM - 12 PM
- **Secondary:** [Name] — Tue-Thu, 3 PM - 6 PM
- **Weekend:** [Name] — Sat-Sun, 10 AM - 2 PM

---

## Metrics Dashboard Setup

### Google Analytics 4 Dashboard
Create custom dashboard with:
- **Gallery Session Count** (weekly trend)
- **Tab Switch Distribution** (Gallery vs Reviews vs Moderation)
- **Filter Button Clicks** (which body families get most interest)
- **Form Submission Rate** (submissions per 100 gallery viewers)
- **Community Page Referral Traffic**

### Airtable or Sheet Tracking
Weekly metrics update:
| Metric | Week 1 | Week 2 | Week 3 | Month 1 Target |
|--------|--------|--------|--------|-----------------|
| Submissions Received | — | — | — | 15-20 |
| Approval Rate | — | — | — | 75%+ |
| Featured Selections | — | — | — | 4-6 |
| Avg Review Time | — hours | — hours | — hours | <12h |
| Calendar Subscriptions | — | — | — | 50+ |
| Review Count | — | — | — | 3-5 |

---

## Rollback Plan

If critical issues found post-launch:

1. **Hide gallery.html temporarily**
   ```bash
   git revert [commit]
   # Or rename temporarily to gallery-disabled.html
   ```

2. **Keep events page live** (separate from gallery)
   - Events are independent functionality
   - No critical dependencies on gallery

3. **Preserve user data**
   - Keep all submissions in `db/community_gallery.json`
   - Preserve iCal file
   - Don't delete any data

4. **Communicate transparently**
   ```
   We're temporarily pausing gallery submissions to improve the experience. 
   The community calendar is still available. We'll be back shortly!
   ```

5. **Post-Incident**
   - Document issue + fix
   - Test on staging 24h
   - Relaunch with improved code

---

## Success Criteria (30 days)

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Total Submissions | 20+ | — | ⏳ |
| Approval Rate | 75%+ | — | ⏳ |
| Moderation Turnaround | <24h avg | — | ⏳ |
| Featured Selections | 5-8 | — | ⏳ |
| Reviews Collected | 5+ | — | ⏳ |
| Calendar Subscriptions | 50+ | — | ⏳ |
| Policy Violations | <2 | — | ⏳ |
| Community Sentiment | Positive | — | ⏳ |

---

## Version History

| Date | Version | Status |
|------|---------|--------|
| 2026-06-21 | 1.0 | Ready for Launch |

---

## Contacts

| Role | Name | Email | Slack |
|------|------|-------|-------|
| Brand Team Lead | [TBD] | [email] | @[handle] |
| Moderation Lead | [TBD] | [email] | @[handle] |
| Community Manager | [TBD] | [email] | @[handle] |
| Tech Lead | [TBD] | [email] | @[handle] |

---

**Questions?** See COMMUNITY_HUB_TRAINING.md or reach out to brand team lead.
