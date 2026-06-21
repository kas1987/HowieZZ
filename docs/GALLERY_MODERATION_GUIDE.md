# ZELEX Gallery Moderation Guide

**Quick Start:** 24-hour review window | Approve/Reject decision per submission | Track metrics

---

## Access & Tools

### Moderation Queue
- **URL:** Internal dashboard (requires moderator auth)
- **Data Source:** `db/community_gallery.json` → `submissions` array
- **Status Values:** `approved` | `rejected` | `pending` | `flagged`
- **Update Workflow:** Edit JSON + push to git (or backend API if deployed)

### Submission Status Lifecycle

```
User Submits
    ↓
[PENDING] — 0-24 hours for review
    ↓
[APPROVED/REJECTED] — Decision notification sent
    ↓
[APPROVED] → Gallery published
[REJECTED] → Feedback email sent; can resubmit after 7 days
```

---

## Approval Criteria Checklist

### Content Quality ✓
- [ ] Image is clear and well-lit (can see ZELEX product clearly)
- [ ] Photo is in focus (not blurry, not rotated)
- [ ] Framing shows product context (setup, outfit, display, etc.)
- [ ] No watermarks from other brands/photographers
- [ ] Resolution adequate for thumbnail + full-size display

### Brand Safety ✓
- [ ] Product is ZELEX (not competitor brands in prominent focus)
- [ ] Positive brand context (styling, care, appreciation)
- [ ] No explicit, violent, or hateful content
- [ ] No political messaging or controversial context
- [ ] Respects regional laws (e.g., privacy, consent for location/group photos)

### Creator Verification ✓
- [ ] Creator is registered collector (cross-reference collector_id)
- [ ] Account history is positive (if available)
- [ ] No spam/self-promotion history
- [ ] Profile includes coherent history of collection engagement

### Metadata Completeness ✓
- [ ] Title is descriptive and under 100 characters
- [ ] Description explains the photo (setup, story, technique)
- [ ] Tags are relevant and accurate
- [ ] Body family correctly identified
- [ ] Region is filled in (for geographic diversity)

---

## Common Decision Scenarios

### ✅ APPROVE

**Example 1: Product Showcase**
```
Title: "K-Series Styling with Natural Window Light"
Description: "My K-Series with custom outfit in natural daylight. Focus on fabric texture and articulation."
Tags: k-series, styling, natural-light, fabric
Body Family: The Classic
Region: North America
→ APPROVE
Reason: Clear product, professional lighting, coherent tags, verified creator
```

**Example 2: Setup Display**
```
Title: "Empress Collector Setup"
Description: "Home display featuring Empress body with custom shelving. Took months to arrange!"
Tags: empress, display, collection, setup
Body Family: The Empress
Region: Europe
→ APPROVE
Reason: Authentic collector story, good composition, diverse region, tagged accurately
```

**Example 3: Technical Comparison**
```
Title: "Muse Head Comparison: Three Options"
Description: "Side-by-side of different head options on same Muse body to help new collectors."
Tags: muse, heads, comparison, reference
Body Family: The Muse
Region: Asia Pacific
→ APPROVE
Reason: Educational value, clear comparison, helps community, professional framing
Featured? YES (high community value)
```

### ❌ REJECT

**Example 1: Poor Lighting**
```
Title: "my doll"
Description: "here she is"
Image: Blurry, dark, hard to see detail
→ REJECT
Reason: "Photos should be clear and well-lit so we can see the product details. Try photographing near a window or with studio lighting. Feel free to resubmit!"
```

**Example 2: Competitor Focus**
```
Title: "Doll Collection"
Description: "My collection with some ZELEX and other brands"
Image: Competitor dolls prominent, ZELEX secondary
→ REJECT
Reason: "Gallery focuses on ZELEX products. If ZELEX is featured, make it the primary focus of the photo and resubmit!"
```

**Example 3: Unverified Creator**
```
Title: "Beautiful Setup"
Description: "just sharing this nice display"
Creator: Unverified account, no purchase history
→ REJECT
Reason: "Submissions require a verified collector account. Purchase a ZELEX product or contact us to get verified, then resubmit your photos!"
```

**Example 4: Policy Violation**
```
Title: "Political Stance with Dolls"
Description: "[Overtly political message]"
Image: Dolls with controversial symbols
→ REJECT + FLAG
Reason: Immediate rejection, no resubmission allowed
Action: Flag moderator; consider account review for repeat violations
```

### 🟡 REQUEST CHANGES

**Example 1: Promising but Incomplete**
```
Title: "my setup"
Description: [Blank or minimal]
Image: Good quality photo, but lacks context
→ REQUEST CHANGES
Feedback: "Great photo! Could you provide more detail about your setup? How did you style it? What body family is this? Reply with more info and we'll approve it!"
```

**Example 2: Needs Better Tagging**
```
Title: "ZELEX Styling"
Description: "Custom outfit with natural lighting"
Tags: [missing/vague]
Body Family: [not filled]
Image: Excellent quality
→ REQUEST CHANGES
Feedback: "Love this photo! Just need you to identify the body family and add a few tags (like 'styling', 'natural-light', region). Reply with those details and we'll feature it!"
```

**Example 3: Regional Context Missing**
```
Title: "Photographer's Perspective"
Description: "Professional studio shot of my collection"
Tags: all correct
Region: [blank]
→ REQUEST CHANGES
Feedback: "Professional work! Which region are you in? Add that and we'll get this featured."
```

---

## Moderation Workflow

### Daily (15-30 min check-in)

1. **Open moderation dashboard**
   - Filter by `status: pending`
   - Sort by `submitted_date` (oldest first)

2. **Per Submission (2-3 min each):**
   - View full image + metadata
   - Check approval criteria checklist above
   - Make decision: APPROVE / REJECT / REQUEST CHANGES
   - If approved: add to featured candidates if relevant
   - If rejected: compose feedback email
   - Update status in JSON + push

3. **Close-out**
   - Post rejected/pending count to #moderation Slack
   - Flag any policy violations for team review

### Weekly (Friday, 30 min)

1. **Audit Approved Submissions**
   - Scan recent approvals for patterns
   - Ensure consistent standards

2. **Feature Selection**
   - Review submissions with 40+ likes
   - Select 4-6 for featured carousel
   - Update `featured: true` in JSON
   - Prepare social media captions

3. **Metrics Check**
   - Count submissions this week
   - Approval rate (target: 75%+)
   - Featured/approved ratio
   - Report to brand team

### Monthly (1 hour)

1. **Team Sync**
   - Review rejection feedback patterns
   - Identify common issues (lighting, framing, etc.)
   - Adjust guidelines if needed

2. **Creator Communication**
   - Thank featured submissions (email or Discord)
   - Respond to appeals from rejected creators
   - Invite top contributors to moderation team

3. **Content Planning**
   - Pick featured submissions for social media
   - Plan social calendar (Instagram, TikTok)
   - Create behind-the-scenes posts

---

## Rejection Email Templates

### Poor Quality/Lighting
```
Subject: Your Gallery Submission — Ready to Resubmit?

Hi [Creator Name],

Thanks for sharing your photo! We loved your idea, but the lighting makes 
it hard to see the product details. 

Next time, try:
• Photographing near a window (natural light is great)
• Using a desk lamp or ring light
• Avoiding harsh shadows on the product

We'd love to see this again with better lighting. Reply to this email 
with your updated photo, or visit gallery.html to submit again!

— ZELEX Community Team
```

### Needs More Context
```
Subject: Your Gallery Submission — Add Context & Resubmit

Hi [Creator Name],

Your photo looks great! We just need a bit more info to feature it:

1. What body family is this? (Classic/Icon/Muse/Siren/Empress/Sculpt)
2. Can you describe your setup or styling approach?
3. What region are you in?

Reply with those details and we'll approve it right away!

— ZELEX Community Team
```

### Policy Violation (No Resubmit)
```
Subject: Gallery Submission — Unable to Approve

Hi [Creator Name],

Your submission doesn't fit our community guidelines. We focus on 
celebrating ZELEX products and collector creativity in a safe, positive space.

If you have questions, reach out to our support team via contact.html.

— ZELEX Community Team
```

---

## Escalation Scenarios

### Harassment / Threats
- [ ] Screenshot submission + email
- [ ] Forward to brand team lead immediately
- [ ] Consider user account review
- [ ] Do NOT approve; do NOT respond to creator

### Repeated Policy Violations
- [ ] After 2nd rejection: send warning email
- [ ] After 3rd rejection: consider account suspension
- [ ] Document pattern for leadership review

### Impersonation / Fake Account
- [ ] Flag immediately for team review
- [ ] Reject submission
- [ ] Check account history for other suspicious submissions
- [ ] Escalate to trust & safety team

### Unclear Decision
- [ ] Ask 2nd moderator opinion
- [ ] Check guidelines above; if still unclear, defer
- [ ] Message creator: "We're reviewing your submission. Thanks for your patience!"
- [ ] Follow up within 48 hours

---

## Metrics to Track

### Per Submission
- `submission_id` — unique identifier
- `submitted_date` — when uploaded
- `status` — approved/rejected/pending
- `approval_date` — decision made
- `review_time_hours` — submitted → approved/rejected
- `featured` — boolean
- `likes` — engagement count

### Per Moderator (weekly)
- Submissions reviewed (target: 15-20/week)
- Approval rate (target: 70-80%)
- Average review time (target: 8-12 hours)
- Featured selections (target: 4-6/week)

### Overall (monthly)
- Total submissions (running count toward 100+ Q3 target)
- Approval rate trend
- Most popular body families
- Top regions contributing
- Featured submissions performance (social shares, engagement)

---

## Tools & Setup

### Local Development
```bash
# Edit submissions in JSON
nano db/community_gallery.json

# After changes:
git add db/community_gallery.json
git commit -m "mod: approve submission [id]"
git push

# Verify on staging:
# → http://localhost:8000/gallery.html
```

### Contact Form Integration
When a submission comes in via the form endpoint, the backend should:
1. Store with `status: pending`
2. Notify moderators (Slack webhook or email)
3. Auto-reply to creator: "Thanks! Your submission is under review. We'll respond within 24 hours."

---

## FAQ

**Q: How long do I have to review?**
A: Target 24 hours; hard limit 48 hours max. If you can't meet this, notify the team.

**Q: What if a creator appeals a rejection?**
A: Give them 1 appeal within 7 days. Review with a 2nd moderator. Decision is final.

**Q: Can I approve/reject without viewing the full image?**
A: No. Always view the full resolution image, metadata, and creator profile before deciding.

**Q: What if a submission is borderline?**
A: Request changes rather than rejecting. Give creator the best chance to succeed.

**Q: How do I handle timezone issues for events in the calendar?**
A: Events are listed in UTC with conversion guides (EST, PST, etc.). Creators choose their timezone when RSVP'ing.

---

## Resources

| Resource | Location |
|----------|----------|
| Gallery submissions | `db/community_gallery.json` |
| Gallery page | `gallery.html` |
| Moderation dashboard | TBD (internal only) |
| Community guidelines | `gallery.html#community-guidelines` |
| Contact form | `contact.html?src=gallery` |

---

**Version:** 1.0 | **Last Updated:** 2026-06-21 | **Next Review:** 2026-07-21
