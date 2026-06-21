/* ============================================================
   PII Scrubber & Audit Module — ZELEX Character Atlas

   Detects and removes personally identifiable information
   from analytics payloads before they enter dataLayer.

   This is a defense-in-depth layer. Primary responsibility
   is on application code to NOT emit PII; this scrubber
   catches accidental leaks.
   ============================================================ */

window.ZX = window.ZX || {};

ZX.PIIScrubber = (function() {
  const MODULE_NAME = '[PIIScrubber]';

  // Patterns for common PII — these are heuristic, not foolproof.
  // Each pattern assumes a weak implementation; real PII detection is harder.
  const PII_PATTERNS = {
    email: /([a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})/,
    phone: /(\+?1?[-.\s]?(\d{3})[-.\s]?(\d{3})[-.\s]?(\d{4}))/,
    phone_intl: /(\+\d{1,3}[-.\s]?\d{4,}[-.\s]?\d{4,})/,
    ssn: /(\d{3}-\d{2}-\d{4})/,
    postal: /(\d{5}[-\s]?\d{4}|\d{5})/,  // US ZIP
    address: /(?:street|st|avenue|ave|road|rd|boulevard|blvd|drive|dr|lane|ln|court|ct|circle|cir)\s+/i,
    credit_card: /(\d{4}[-\s]?){3}\d{4}/,
    url_query: /[?&]([a-zA-Z0-9_]+)=([^&]+)/  // Query param inspection
  };

  // Field names that should never contain user-submitted data.
  const PROHIBITED_FIELDS = new Set([
    'email', 'phone', 'address', 'zip_code', 'postal_code',
    'name', 'first_name', 'last_name', 'full_name',
    'street', 'city', 'state', 'country',
    'credit_card', 'ccn', 'card_number',
    'ssn', 'social_security',
    'dob', 'birthdate', 'age',
    'user_id', 'customer_id', 'account_id',
    'password', 'secret', 'token', 'api_key',
    'ip_address', 'ip',
    'user_input', 'raw_input', 'form_data'
  ]);

  // Fields that CAN safely contain categories/descriptors (not values).
  const SAFE_CATEGORY_FIELDS = new Set([
    'form_field',           // 'email', 'phone' OK; 'user@example.com' NOT OK
    'form_name',            // 'contact', 'inquiry' OK
    'filter_field',         // 'body_code', 'series' OK
    'option_category',      // 'color', 'size' OK
    'event_name',           // Event label OK
    'media_type',           // 'image', 'pdf' OK
    'error_type'            // 'validation_error' OK
  ]);

  let auditLog = [];
  let auditEnabled = false;

  function isEmail(value) {
    return PII_PATTERNS.email.test(String(value));
  }

  function isPhone(value) {
    return PII_PATTERNS.phone.test(String(value)) || PII_PATTERNS.phone_intl.test(String(value));
  }

  function isPostalCode(value) {
    return PII_PATTERNS.postal.test(String(value));
  }

  function isAddress(value) {
    return PII_PATTERNS.address.test(String(value));
  }

  function isCreditCard(value) {
    return PII_PATTERNS.credit_card.test(String(value));
  }

  function isSSN(value) {
    return PII_PATTERNS.ssn.test(String(value));
  }

  function isPII(value) {
    const strVal = String(value || '').trim();
    return isEmail(strVal) || isPhone(strVal) || isPostalCode(strVal) ||
           isAddress(strVal) || isCreditCard(strVal) || isSSN(strVal);
  }

  function audit(fieldKey, fieldValue, reason) {
    if (!auditEnabled) return;
    auditLog.push({
      field: fieldKey,
      value: String(fieldValue).slice(0, 20) + '...',  // Truncate in audit log
      reason,
      timestamp: new Date().toISOString()
    });
  }

  function scrubPayload(eventPayload) {
    if (!eventPayload || typeof eventPayload !== 'object') return eventPayload;

    const scrubbed = Object.assign({}, eventPayload);
    const removed = [];
    const sanitized = [];

    // Iterate over all fields in the payload
    Object.keys(scrubbed).forEach(key => {
      const value = scrubbed[key];

      // Skip falsy values
      if (value == null || value === '' || value === false) return;

      const lowercaseKey = key.toLowerCase();

      // Rule 1: Explicitly prohibited field names
      if (PROHIBITED_FIELDS.has(lowercaseKey)) {
        delete scrubbed[key];
        removed.push(key);
        audit(key, value, 'prohibited_field');
        return;
      }

      // Rule 2: Detect PII patterns in any field value
      if (typeof value === 'string' && isPII(value)) {
        delete scrubbed[key];
        removed.push(key);
        audit(key, value, 'pii_pattern_detected');
        return;
      }

      // Rule 3: For category fields, allow descriptors but not PII values
      if (SAFE_CATEGORY_FIELDS.has(lowercaseKey)) {
        if (typeof value === 'string' && isPII(value)) {
          delete scrubbed[key];
          removed.push(key);
          audit(key, value, 'pii_in_category_field');
        }
        return;
      }

      // Rule 4: Truncate error messages (max 180 chars)
      if (key === 'error_message' && typeof value === 'string') {
        const truncated = value.slice(0, 180);
        if (truncated !== value) {
          scrubbed[key] = truncated;
          sanitized.push(key);
        }
      }
    });

    // Optionally log scrubbing action
    if (removed.length > 0 || sanitized.length > 0) {
      if (removed.length > 0) {
        console.warn(MODULE_NAME, 'Removed PII fields:', removed);
      }
      if (sanitized.length > 0) {
        console.debug(MODULE_NAME, 'Sanitized fields:', sanitized);
      }
    }

    return scrubbed;
  }

  function enableAudit() {
    auditEnabled = true;
    auditLog = [];
    console.debug(MODULE_NAME, 'Audit enabled.');
  }

  function disableAudit() {
    auditEnabled = false;
    console.debug(MODULE_NAME, 'Audit disabled.');
  }

  function getAuditLog() {
    return auditLog.slice();  // Return copy
  }

  function clearAuditLog() {
    auditLog = [];
  }

  function exportAudit(format = 'json') {
    if (format === 'csv') {
      const headers = ['field', 'value', 'reason', 'timestamp'];
      const rows = auditLog.map(a => [a.field, a.value, a.reason, a.timestamp]);
      const csv = [headers, ...rows].map(r => r.map(v => `"${v}"`).join(',')).join('\n');
      return csv;
    }
    return JSON.stringify(auditLog, null, 2);
  }

  function validateEvent(eventName, eventPayload) {
    const report = {
      event: eventName,
      valid: true,
      issues: [],
      warnings: [],
      errors: []
    };

    if (!eventPayload || typeof eventPayload !== 'object') {
      report.valid = false;
      report.errors.push('Payload is not an object');
      return report;
    }

    // Check mandatory fields
    const mandatory = ['event', 'session_id', 'ts', 'page', 'path', 'source'];
    mandatory.forEach(field => {
      if (!eventPayload[field]) {
        report.warnings.push(`Missing mandatory field: ${field}`);
      }
    });

    // Scan for PII
    Object.keys(eventPayload).forEach(key => {
      const value = eventPayload[key];
      if (typeof value === 'string' && isPII(value)) {
        report.valid = false;
        report.errors.push(`Field '${key}' contains PII`);
      }
    });

    return report;
  }

  // Export scrubber utilities
  return {
    scrubPayload,
    validateEvent,
    isEmail,
    isPhone,
    isAddress,
    isCreditCard,
    isSSN,
    isPII,
    enableAudit,
    disableAudit,
    getAuditLog,
    clearAuditLog,
    exportAudit
  };
})();

// Hook into ZX.track() to automatically scrub before emission
(function() {
  const originalTrack = window.ZX && window.ZX.track;
  if (typeof originalTrack === 'function') {
    window.ZX.track = function(eventName, payload) {
      const scrubbed = ZX.PIIScrubber.scrubPayload(payload);
      return originalTrack.call(this, eventName, scrubbed);
    };
    console.debug('[PIIScrubber] Installed automatic scrubbing hook.');
  }
})();
