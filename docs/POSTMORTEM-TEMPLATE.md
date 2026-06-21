# Post-Mortem Template

**Incident ID**: [AUTO-GENERATED or MANUAL]  
**Date**: [YYYY-MM-DD]  
**Duration**: [HH:MM] (from detection to resolution)  
**Severity**: [P1 / P2 / P3]  
**Status**: [DRAFT / REVIEWED / CLOSED]

---

## Executive Summary

[1–2 sentences describing what happened and impact to end users]

**Example**: "On 2026-06-21 at 14:30 UTC, the Shopify sync workflow failed due to expired API credentials, preventing character catalog updates for 2 hours. 12 newly launched characters were unavailable on the Browse page."

---

## Impact

| Metric | Value |
|---|---|
| **Users Affected** | [number or estimate] |
| **Downtime** | [HH:MM] |
| **Revenue Lost** | [estimate or N/A] |
| **Data Lost** | [Yes/No, describe if yes] |
| **Security Incident** | [Yes/No] |

---

## Timeline

| Time (UTC) | Event | Owner |
|---|---|---|
| HH:MM | Incident detected (alert / manual report) | [Name] |
| HH:MM | Initial triage completed | [Name] |
| HH:MM | Root cause identified | [Name] |
| HH:MM | Mitigation started | [Name] |
| HH:MM | Incident resolved | [Name] |
| HH:MM | Communication sent to users | [Name] |

---

## Root Cause Analysis

### What Happened?

[Detailed narrative of the incident. What was the sequence of events?]

**Example**: "Shopify API token expired on 2026-06-20. The sync workflow continued to retry with the stale token, which resulted in authentication failures. The failure notification was sent to Slack but was missed due to message volume. On 2026-06-21 morning, the next scheduled sync failed and was caught during the daily health check."

### Why Did It Happen?

[Investigate and list root causes. Use the "5 Whys" technique.]

1. **Why did the token expire?**
   - Shopify tokens are configured to expire every 12 months for security.

2. **Why wasn't it rotated?**
   - There was no automated reminder or alert 30 days before expiration.

3. **Why wasn't the alert caught?**
   - On-call was in different timezone and missed the Slack message.

4. **Why wasn't there a secondary alert?**
   - Only Slack was configured; no email or SMS backup.

### Contributing Factors

- [ ] Insufficient monitoring (no alert on auth failures)
- [ ] No notification redundancy (only Slack)
- [ ] Manual token rotation (should be automated)
- [ ] Lack of documentation (on-call didn't know rotation procedure)
- [ ] No runbook for this scenario
- [ ] Unclear escalation path

---

## Lessons Learned

### What Went Well

- Fast detection during daily health check
- Incident resolved within 2 hours
- Clear communication to team

### What Could Be Better

1. **Automated token rotation**: Implement 30-day pre-expiration alert + auto-refresh
2. **Alert redundancy**: Slack + email + SMS for critical incidents
3. **Monitoring coverage**: Add authentication failure alert to Uptime Robot
4. **Documentation**: Add "Shopify Sync Auth Failure" runbook to OPERATIONS.md
5. **On-call training**: Ensure new team members know token rotation procedure

---

## Action Items (Follow-Up)

| Action | Owner | Due Date | Priority |
|---|---|---|---|
| Implement Shopify token auto-rotation | DevOps | 2026-07-15 | P1 |
| Add auth failure alert to Uptime Robot | DevOps | 2026-06-28 | P2 |
| Add runbook for Shopify auth errors | On-Call Lead | 2026-06-24 | P2 |
| Update on-call training checklist | Team Lead | 2026-06-25 | P3 |
| Add alert to email + SMS channel | DevOps | 2026-07-05 | P2 |

---

## Prevention Measures

### Immediate (Done)

- [ ] Rotated Shopify API token
- [ ] Added authentication failure to monitoring
- [ ] Notified on-call team of procedure

### Short-Term (This Sprint)

- [ ] Implement 30-day pre-expiration alert
- [ ] Add email notification channel
- [ ] Create runbook in OPERATIONS.md

### Long-Term (Q3)

- [ ] Automate token rotation via GitHub Secrets rotation API
- [ ] Build dashboard showing credential expiration dates
- [ ] Establish quarterly credential audit process

---

## Communication Log

### Internal

- **Time**: 14:35 UTC
- **Channel**: Slack `#zelex-ops`
- **Message**: "Alert: Shopify sync failed. Investigating."
- **Follow-up**: 15:20 UTC — "Root cause: expired token. Rotating now."
- **Resolution**: 16:30 UTC — "Sync restored. Catalog updated."

### External (if user-facing)

- **Status Page**: [Updated with incident notice]
- **Email**: [Sent to subscribers if applicable]
- **Social**: [Twitter/LinkedIn post if major incident]

---

## Appendix

### Relevant Logs

```
[Paste relevant log excerpts here]

Example:
2026-06-21T14:32:00Z [ERROR] Shopify API: 401 Unauthorized
2026-06-21T14:32:15Z [RETRY] Attempt 2 of 5...
2026-06-21T14:35:00Z [FAILURE] All retries exhausted. Notifying on-call.
```

### Monitoring Configuration

**Alert**: Shopify Sync Authentication Failure
```yaml
# Slack notification
channel: #zelex-ops
severity: P2
condition: Shopify API returns 401
threshold: 1 failure in 5 min
```

### References

- Runbook: [OPERATIONS.md § Shopify Sync Failed](#shopify-sync-failed)
- Configuration: [.github/workflows/shopify-sync.yml](../.github/workflows/shopify-sync.yml)
- Incident tracker: [GitHub Issues](https://github.com/kas1987/HowieZZ/issues)

---

## Sign-Off

| Role | Name | Date | Signature |
|---|---|---|---|
| **Incident Commander** | [Name] | [Date] | [Approval] |
| **On-Call Lead** | [Name] | [Date] | [Approval] |
| **Engineering Lead** | [Name] | [Date] | [Approval] |

---

**Template Version**: 1.0  
**Last Updated**: 2026-06-21  
**Next Review**: Every incident (required), Quarterly (process review)
