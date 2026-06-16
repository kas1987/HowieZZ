# SWOT + Gap Review (2026-06-16)

## Scope
- Internal HTML stack reviewed: root site pages and newly added community hub.
- External benchmark target requested: zelex.com / zelexdoll.com.

## Data Availability Note
- Direct content extraction for zelex.com / zelexdoll.com was partially blocked by Shop App redirect / anti-bot behavior during automated fetch.
- Alternative used: current in-repo sitemap, existing conversion flows, and publicly reachable redirect behavior.

## SWOT: Current HowieZZ HTML Experience

### Strengths
- Strong conversion funnel is already present: Home -> Quiz -> Compare -> Contact.
- Body architecture taxonomy is deeply modeled and consistent across Browse, Family, Body, Character, and Options pages.
- Shared runtime and design tokens create coherent navigation/visual behavior.
- Governance and CI checks are active (site validator + PDR_PATH guard).

### Weaknesses
- Community entry points were previously fragmented (no dedicated community front door).
- Social/Discord/blog access pathways were not centrally explained.
- No explicit "where to go for what" guidance for collectors vs customers.
- v2 packaging previously required manual copy operations without deterministic manifest evidence.

### Opportunities
- Community hub can increase repeat engagement and reduce support friction.
- Structured collector channels (Blog, Magazine, Discord, Social directory) can improve trust and onboarding.
- Event instrumentation on community CTAs enables measurement of channel demand.
- Packaging automation + checksums improves release discipline and handoff quality.

### Threats
- Without a clear official directory, users can be exposed to impersonation/scam channels.
- Redirect/protection behavior on external storefront endpoints can break discovery expectations.
- Community channels without clear moderation paths can create compliance and reputational risk.
- Fragmented channel links can dilute conversion tracking and CRM attribution.

## Gap Review: Missing vs Desired ZELEX.com-Like Presence

### Previously Missing (Now Addressed)
- Dedicated Community landing page with explicit channel lanes.
- Explicit collector/customer routing for Blogs, Mags, Discord, Social access.
- Single place for access-request and moderation-help CTAs.

### Still Recommended
- Confirm and publish canonical public social URLs when verified by brand team.
- Add a monthly "Community Bulletin" archive index page.
- Add a simple status feed for planned events (drops, AMAs, magazine issue dates).
- Add anti-impersonation notice with official handle verification list.

## Delivered in This Pass
- New [community.html](community.html) hub page.
- Nav/footer integration to expose Community globally.
- New packaging script [scripts/refresh_v2_html.ps1](scripts/refresh_v2_html.ps1).
- Manifest and checksum generation in [v2 HTML](v2%20HTML).

## KPI Suggestions
- community_view count per week.
- community_handoff_click by channel lane (blog, magazine, discord, social).
- contact submissions with src=community parameters.
- return sessions that originate from community entry paths.
