/* ============================================================
   Event Tracking Module — ZELEX Character Atlas

   Consolidated tracking for all user interactions:
   - Navigation & page views
   - Browse & filter
   - Comparison tool
   - Quiz flow
   - Contact form
   - Configurator
   - Community engagement
   - Error handling

   Uses global ZX.track() for dataLayer emission.
   ============================================================ */

window.ZX = window.ZX || {};

ZX.EventTracker = (function() {
  const MODULE_NAME = '[EventTracker]';
  const DEBUG = (function() {
    try {
      return String(new URLSearchParams(location.search).get('zx_analytics_debug') || '').toLowerCase() === '1';
    } catch {
      return false;
    }
  })();

  function log(...args) {
    if (DEBUG) console.debug(MODULE_NAME, ...args);
  }

  // ========== NAVIGATION & PAGE VIEWS ==========

  function trackPageView(context = 'navigation') {
    const pageName = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
    log('page_view', pageName, context);
    ZX.track('page_view', {
      context,
      source_page: pageName.replace('.html', '')
    });
  }

  function trackNavigate(sourcePageName, ctaLabel, intent = null) {
    log('navigate', sourcePageName, ctaLabel, intent);
    ZX.track('navigate', {
      source_page: sourcePageName.replace('.html', ''),
      cta: ctaLabel,
      intent,
      context: 'navigation'
    });
  }

  function trackNavigateSeries(seriesName, sourcePageName) {
    log('navigate_series', seriesName, sourcePageName);
    ZX.track('navigate_series', {
      series: seriesName,
      source_page: sourcePageName.replace('.html', ''),
      context: 'navigation'
    });
  }

  function trackNavigateFamily(familyName, sourcePageName) {
    log('navigate_family', familyName, sourcePageName);
    ZX.track('navigate_family', {
      family: familyName,
      source_page: sourcePageName.replace('.html', ''),
      context: 'navigation'
    });
  }

  function trackNavigateBody(bodyCode, familyName, sourcePageName) {
    log('navigate_body', bodyCode, familyName, sourcePageName);
    ZX.track('navigate_body', {
      body_code: bodyCode,
      family: familyName,
      source_page: sourcePageName.replace('.html', ''),
      context: 'navigation'
    });
  }

  function trackNavigateCharacter(characterId, bodyCode, seriesName, sourcePageName) {
    log('navigate_character', characterId, bodyCode, sourcePageName);
    ZX.track('navigate_character', {
      character_id: characterId,
      body_code: bodyCode,
      series: seriesName,
      source_page: sourcePageName.replace('.html', ''),
      context: 'navigation'
    });
  }

  // ========== BROWSE & FILTER ==========

  function trackBrowseView(filterApplied = false) {
    log('browse_view', filterApplied);
    ZX.track('browse_view', {
      filter_applied: filterApplied,
      view_state: 'browse'
    });
  }

  function trackBrowseFilterApply(filterField, filterValue, bodyCodes = null) {
    log('browse_filter_apply', filterField, filterValue);
    const payload = {
      filter_field: filterField,
      filter_value: filterValue,
      context: 'interaction'
    };
    if (bodyCodes) {
      payload.body_codes = (Array.isArray(bodyCodes) ? bodyCodes : [bodyCodes]).join(',');
      payload.compare_count = (Array.isArray(bodyCodes) ? bodyCodes : [bodyCodes]).length;
    }
    ZX.track('browse_filter_apply', payload);
  }

  function trackBrowseFilterClear() {
    log('browse_filter_clear');
    ZX.track('browse_filter_clear', { context: 'interaction' });
  }

  function trackBrowseSortApply(sortField, sortOrder) {
    log('browse_sort_apply', sortField, sortOrder);
    ZX.track('browse_sort_apply', {
      sort_field: sortField,
      sort_order: sortOrder,
      context: 'interaction'
    });
  }

  function trackSeriesView(seriesName) {
    log('series_view', seriesName);
    ZX.track('series_view', {
      series: seriesName,
      view_state: 'detail',
      context: 'content'
    });
  }

  function trackBodyView(bodyCode, familyName, seriesName = null, heightCm = null, cup = null) {
    log('body_view', bodyCode, familyName);
    const payload = {
      body_code: bodyCode,
      family: familyName,
      view_state: 'detail',
      context: 'content'
    };
    if (seriesName) payload.series = seriesName;
    if (heightCm) payload.body_height_cm = heightCm;
    if (cup) payload.body_cup = cup;
    ZX.track('body_view', payload);
  }

  function trackCharacterView(characterId, bodyCode, seriesName = null, familyName = null, personaName = null) {
    log('character_view', characterId, bodyCode);
    const payload = {
      character_id: characterId,
      body_code: bodyCode,
      view_state: 'detail',
      context: 'content'
    };
    if (seriesName) payload.series = seriesName;
    if (familyName) payload.family = familyName;
    if (personaName) payload.persona_name = personaName;
    ZX.track('character_view', payload);
  }

  // ========== COMPARISON TOOL ==========

  function trackCompareView(bodyCodes = []) {
    log('compare_view', bodyCodes);
    const payload = {
      view_state: 'compare',
      context: 'interaction'
    };
    if (bodyCodes && bodyCodes.length > 0) {
      payload.body_codes = (Array.isArray(bodyCodes) ? bodyCodes : [bodyCodes]).join(',');
      payload.compare_count = (Array.isArray(bodyCodes) ? bodyCodes : [bodyCodes]).length;
    }
    ZX.track('compare_view', payload);
  }

  function trackCompareAdd(bodyCode, sourcePageName = null, compareCount = null) {
    log('compare_add', bodyCode, compareCount);
    const payload = {
      body_code: bodyCode,
      context: 'interaction'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    if (compareCount != null) payload.compare_count = compareCount;
    ZX.track('compare_add', payload);
  }

  function trackCompareRemove(bodyCode, compareCount = null) {
    log('compare_remove', bodyCode, compareCount);
    const payload = {
      body_code: bodyCode,
      context: 'interaction'
    };
    if (compareCount != null) payload.compare_count = compareCount;
    ZX.track('compare_remove', payload);
  }

  function trackCompareReset(previousCount = null) {
    log('compare_reset', previousCount);
    const payload = { context: 'interaction' };
    if (previousCount != null) payload.compare_count = previousCount;
    ZX.track('compare_reset', payload);
  }

  function trackCompareMetricInspect(metricType, bodyCode = null) {
    log('compare_metric_inspect', metricType, bodyCode);
    const payload = {
      metric_type: metricType,
      context: 'interaction'
    };
    if (bodyCode) payload.body_code = bodyCode;
    ZX.track('compare_metric_inspect', payload);
  }

  function trackCompareHandoffClick(intent, sourcePageName = null, bodyCodes = [], compareCount = null) {
    log('compare_handoff_click', intent, compareCount);
    const payload = {
      intent,
      context: 'interaction'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    if (bodyCodes && bodyCodes.length > 0) {
      payload.body_codes = (Array.isArray(bodyCodes) ? bodyCodes : [bodyCodes]).join(',');
    }
    if (compareCount != null) payload.compare_count = compareCount;
    ZX.track('compare_handoff_click', payload);
  }

  // ========== QUIZ ==========

  function trackQuizStart(sourcePageName = null) {
    log('quiz_start');
    const payload = { context: 'interaction' };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('quiz_start', payload);
  }

  function trackQuizQuestionView(questionNum) {
    log('quiz_question_view', questionNum);
    ZX.track('quiz_question_view', {
      quiz_question: questionNum,
      context: 'interaction'
    });
  }

  function trackQuizAnswerSelect(questionNum, answerValue) {
    log('quiz_answer_select', questionNum, answerValue);
    ZX.track('quiz_answer_select', {
      quiz_question: questionNum,
      quiz_answer: answerValue,
      context: 'interaction'
    });
  }

  function trackQuizQuestionSkip(questionNum) {
    log('quiz_question_skip', questionNum);
    ZX.track('quiz_question_skip', {
      quiz_question: questionNum,
      context: 'interaction'
    });
  }

  function trackQuizAnswerChange(questionNum, answerValue) {
    log('quiz_answer_change', questionNum, answerValue);
    ZX.track('quiz_answer_change', {
      quiz_question: questionNum,
      quiz_answer: answerValue,
      context: 'interaction'
    });
  }

  function trackQuizComplete(resultFamily, resultCharacterIds, durationSec = null) {
    log('quiz_complete', resultFamily, resultCharacterIds, durationSec);
    const payload = {
      quiz_result_family: resultFamily,
      quiz_result_characters: (Array.isArray(resultCharacterIds) ? resultCharacterIds : [resultCharacterIds]).join(','),
      context: 'interaction'
    };
    if (durationSec != null) payload.quiz_duration_sec = Math.round(durationSec);
    ZX.track('quiz_complete', payload);
  }

  function trackQuizAbandon(currentQuestionNum, durationSec = null) {
    log('quiz_abandon', currentQuestionNum, durationSec);
    const payload = {
      quiz_question: currentQuestionNum,
      context: 'interaction'
    };
    if (durationSec != null) payload.quiz_duration_sec = Math.round(durationSec);
    ZX.track('quiz_abandon', payload);
  }

  function trackQuizResultToContact(resultCharacterIds) {
    log('quiz_result_to_contact', resultCharacterIds);
    ZX.track('quiz_result_to_contact', {
      quiz_result_characters: (Array.isArray(resultCharacterIds) ? resultCharacterIds : [resultCharacterIds]).join(','),
      intent: 'inquire',
      context: 'interaction'
    });
  }

  function trackQuizResultToBrowse() {
    log('quiz_result_to_browse');
    ZX.track('quiz_result_to_browse', {
      intent: 'explore',
      context: 'navigation'
    });
  }

  // ========== CONTACT FORM ==========

  function trackContactView(characterId = null, sourcePageName = null) {
    log('contact_view', characterId);
    const payload = {
      form_name: 'contact',
      context: 'content'
    };
    if (characterId) payload.character_id = characterId;
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('contact_view', payload);
  }

  function trackContactFormFocus(fieldName) {
    log('contact_form_focus', fieldName);
    ZX.track('contact_form_focus', {
      form_name: 'contact',
      form_field: fieldName,
      context: 'interaction'
    });
  }

  function trackContactFormInput(fieldName) {
    log('contact_form_input', fieldName);
    ZX.track('contact_form_input', {
      form_name: 'contact',
      form_field: fieldName,
      context: 'interaction'
    });
  }

  function trackContactFormBlur(fieldName) {
    log('contact_form_blur', fieldName);
    ZX.track('contact_form_blur', {
      form_name: 'contact',
      form_field: fieldName,
      context: 'interaction'
    });
  }

  function trackContactFormValidate(fieldName, errorType = null) {
    log('contact_form_validate', fieldName, errorType);
    const payload = {
      form_name: 'contact',
      form_field: fieldName,
      context: 'interaction'
    };
    if (errorType) payload.form_error = errorType;
    ZX.track('contact_form_validate', payload);
  }

  function trackContactFormSubmit(fieldCount = null) {
    log('contact_form_submit', fieldCount);
    const payload = {
      form_name: 'contact',
      context: 'interaction'
    };
    if (fieldCount != null) payload.form_field_count = fieldCount;
    ZX.track('contact_form_submit', payload);
  }

  function trackContactFormSuccess() {
    log('contact_form_success');
    ZX.track('contact_form_success', {
      form_name: 'contact',
      form_submit_success: true,
      context: 'interaction'
    });
  }

  function trackContactFormError(errorType, errorMessage = null) {
    log('contact_form_error', errorType);
    const payload = {
      form_name: 'contact',
      form_error: errorType,
      error_type: errorType,
      context: 'interaction'
    };
    if (errorMessage) payload.error_message = errorMessage;
    ZX.track('contact_form_error', payload);
  }

  function trackContactMailtoClick(characterId = null) {
    log('contact_mailto_click', characterId);
    const payload = {
      form_name: 'contact',
      context: 'interaction'
    };
    if (characterId) payload.character_id = characterId;
    ZX.track('contact_mailto_click', payload);
  }

  function trackInquiryPrefillDetect(characterId) {
    log('inquiry_prefill_detect', characterId);
    ZX.track('inquiry_prefill_detect', {
      character_id: characterId,
      form_name: 'contact',
      context: 'interaction'
    });
  }

  // ========== CONFIGURATOR ==========

  function trackConfiguratorView(sourcePageName = null) {
    log('configurator_view');
    const payload = {
      view_state: 'configurator',
      context: 'content'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('configurator_view', payload);
  }

  function trackConfiguratorOptionSelect(optionCategory, optionValue) {
    log('configurator_option_select', optionCategory, optionValue);
    ZX.track('configurator_option_select', {
      option_category: optionCategory,
      option_value: optionValue,
      context: 'interaction'
    });
  }

  function trackConfiguratorPreviewUpdate(optionCategory = null) {
    log('configurator_preview_update', optionCategory);
    const payload = { context: 'interaction' };
    if (optionCategory) payload.option_category = optionCategory;
    ZX.track('configurator_preview_update', payload);
  }

  function trackConfiguratorSaveConfig(configHash = null) {
    log('configurator_save_config', configHash);
    const payload = { context: 'interaction' };
    if (configHash) payload.config_hash = configHash;
    ZX.track('configurator_save_config', payload);
  }

  function trackConfiguratorShareConfig(configHash = null) {
    log('configurator_share_config', configHash);
    const payload = { context: 'interaction' };
    if (configHash) payload.config_hash = configHash;
    ZX.track('configurator_share_config', payload);
  }

  function trackConfiguratorToInquiry(configHash = null) {
    log('configurator_to_inquiry', configHash);
    const payload = {
      intent: 'inquire',
      context: 'interaction'
    };
    if (configHash) payload.config_hash = configHash;
    ZX.track('configurator_to_inquiry', payload);
  }

  // ========== MEDIA & DOWNLOADS ==========

  function trackMediaView(mediaType, mediaTitle, characterId = null, bodyCode = null) {
    log('media_view', mediaType, mediaTitle);
    const payload = {
      media_type: mediaType,
      media_title: mediaTitle,
      context: 'content'
    };
    if (characterId) payload.character_id = characterId;
    if (bodyCode) payload.body_code = bodyCode;
    ZX.track('media_view', payload);
  }

  function trackMediaFullScreen(mediaTitle, characterId = null) {
    log('media_full_screen', mediaTitle);
    const payload = {
      media_title: mediaTitle,
      context: 'interaction'
    };
    if (characterId) payload.character_id = characterId;
    ZX.track('media_full_screen', payload);
  }

  function trackMediaCarouselNav(mediaType, mediaIndex = null, mediaCount = null) {
    log('media_carousel_nav', mediaType, mediaIndex);
    const payload = {
      media_type: mediaType,
      context: 'interaction'
    };
    if (mediaIndex != null) payload.media_index = mediaIndex;
    if (mediaCount != null) payload.media_count = mediaCount;
    ZX.track('media_carousel_nav', payload);
  }

  function trackDownloadStart(fileType, downloadUrl, characterId = null) {
    log('download_start', fileType);
    const payload = {
      file_type: fileType,
      download_url: downloadUrl,
      context: 'interaction'
    };
    if (characterId) payload.character_id = characterId;
    ZX.track('download_start', payload);
  }

  function trackDownloadComplete(fileType, fileSizeMb = null) {
    log('download_complete', fileType, fileSizeMb);
    const payload = {
      file_type: fileType,
      context: 'interaction'
    };
    if (fileSizeMb != null) payload.file_size_mb = fileSizeMb;
    ZX.track('download_complete', payload);
  }

  // ========== COMMUNITY & SOCIAL ==========

  function trackCommunityView(sourcePageName = null) {
    log('community_view');
    const payload = {
      view_state: 'community',
      context: 'content'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('community_view', payload);
  }

  function trackCommunityChannelLink(channelName, channelUrl = null) {
    log('community_channel_link', channelName);
    const payload = {
      channel: channelName,
      context: 'interaction'
    };
    if (channelUrl) payload.channel_url = channelUrl;
    ZX.track('community_channel_link', payload);
  }

  function trackCommunityEventView(eventName, channelName = null) {
    log('community_event_view', eventName, channelName);
    const payload = {
      event_name: eventName,
      context: 'content'
    };
    if (channelName) payload.channel = channelName;
    ZX.track('community_event_view', payload);
  }

  function trackCommunityEventRegister(eventName, eventDate = null) {
    log('community_event_register', eventName);
    const payload = {
      event_name: eventName,
      context: 'interaction'
    };
    if (eventDate) payload.event_date = eventDate;
    ZX.track('community_event_register', payload);
  }

  function trackShareClick(shareChannel, characterId = null, bodyCode = null) {
    log('share_click', shareChannel);
    const payload = {
      share_channel: shareChannel,
      context: 'interaction'
    };
    if (characterId) payload.character_id = characterId;
    if (bodyCode) payload.body_code = bodyCode;
    ZX.track('share_click', payload);
  }

  // ========== ERROR HANDLING ==========

  function trackErrorPageLoad(errorType, errorMessage = null) {
    log('error_page_load', errorType);
    const payload = {
      error_type: errorType,
      context: 'error'
    };
    if (errorMessage) payload.error_message = errorMessage;
    ZX.track('error_page_load', payload);
  }

  function trackErrorDataFetch(errorType, errorMessage = null, endpoint = null) {
    log('error_data_fetch', errorType);
    const payload = {
      error_type: errorType,
      context: 'error'
    };
    if (errorMessage) payload.error_message = errorMessage;
    if (endpoint) payload.endpoint = endpoint;
    ZX.track('error_data_fetch', payload);
  }

  function trackErrorFormValidation(formName, fieldName, errorType, errorMessage = null) {
    log('error_form_validation', formName, fieldName, errorType);
    const payload = {
      form_name: formName,
      form_field: fieldName,
      error_type: errorType,
      context: 'error'
    };
    if (errorMessage) payload.error_message = errorMessage;
    ZX.track('error_form_validation', payload);
  }

  function trackErrorAnalyticsDebug(errorType, errorMessage = null) {
    log('error_analytics_debug', errorType);
    const payload = {
      error_type: errorType,
      context: 'error'
    };
    if (errorMessage) payload.error_message = errorMessage;
    ZX.track('error_analytics_debug', payload);
  }

  // ========== ENGAGEMENT METRICS ==========

  function trackScrollDepth(scrollPercentage) {
    log('scroll_depth', scrollPercentage + '%');
    ZX.track('scroll_depth', {
      scroll_percentage: scrollPercentage,
      context: 'engagement'
    });
  }

  function trackTimeOnPage(timeSpentSec) {
    log('time_on_page', timeSpentSec + 's');
    ZX.track('time_on_page', {
      time_spent_sec: Math.round(timeSpentSec),
      context: 'engagement'
    });
  }

  function trackViewportResize(viewportWidth, viewportHeight) {
    log('viewport_resize', viewportWidth + 'x' + viewportHeight);
    ZX.track('viewport_resize', {
      viewport_width: viewportWidth,
      viewport_height: viewportHeight,
      context: 'engagement'
    });
  }

  function trackLinkClick(linkText, linkUrl, sourcePageName = null) {
    log('link_click', linkText, linkUrl);
    const payload = {
      link_text: linkText,
      link_url: linkUrl,
      context: 'interaction'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('link_click', payload);
  }

  // ========== NEWSLETTER ==========

  function trackNewsletterSignupView(sourcePageName = null) {
    log('newsletter_signup_view');
    const payload = {
      form_name: 'newsletter',
      context: 'content'
    };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('newsletter_signup_view', payload);
  }

  function trackNewsletterSignupSubmit() {
    log('newsletter_signup_submit');
    ZX.track('newsletter_signup_submit', {
      form_name: 'newsletter',
      context: 'interaction'
    });
  }

  function trackNewsletterSignupSuccess() {
    log('newsletter_signup_success');
    ZX.track('newsletter_signup_success', {
      form_name: 'newsletter',
      context: 'interaction'
    });
  }

  // ========== INTENT & FUNNEL ==========

  function trackFunnelExplore(intent = null) {
    log('funnel_explore', intent);
    const payload = { context: 'funnel' };
    if (intent) payload.intent = intent;
    ZX.track('funnel_explore', payload);
  }

  function trackFunnelConsider(bodyCode, intent = null) {
    log('funnel_consider', bodyCode, intent);
    const payload = {
      body_code: bodyCode,
      context: 'funnel'
    };
    if (intent) payload.intent = intent;
    ZX.track('funnel_consider', payload);
  }

  function trackFunnelCompare(compareCount) {
    log('funnel_compare', compareCount);
    ZX.track('funnel_compare', {
      compare_count: compareCount,
      context: 'funnel'
    });
  }

  function trackFunnelInquire(characterId = null, sourcePageName = null) {
    log('funnel_inquire', characterId);
    const payload = {
      context: 'funnel'
    };
    if (characterId) payload.character_id = characterId;
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    ZX.track('funnel_inquire', payload);
  }

  function trackFunnelAbandon(sourcePageName = null, timeSpentSec = null) {
    log('funnel_abandon', timeSpentSec);
    const payload = { context: 'funnel' };
    if (sourcePageName) payload.source_page = sourcePageName.replace('.html', '');
    if (timeSpentSec != null) payload.time_spent_sec = Math.round(timeSpentSec);
    ZX.track('funnel_abandon', payload);
  }

  // Public API
  return {
    // Navigation
    trackPageView,
    trackNavigate, trackNavigateSeries, trackNavigateFamily, trackNavigateBody, trackNavigateCharacter,
    // Browse
    trackBrowseView, trackBrowseFilterApply, trackBrowseFilterClear, trackBrowseSortApply,
    trackSeriesView, trackBodyView, trackCharacterView,
    // Comparison
    trackCompareView, trackCompareAdd, trackCompareRemove, trackCompareReset, trackCompareMetricInspect, trackCompareHandoffClick,
    // Quiz
    trackQuizStart, trackQuizQuestionView, trackQuizAnswerSelect, trackQuizQuestionSkip, trackQuizAnswerChange,
    trackQuizComplete, trackQuizAbandon, trackQuizResultToContact, trackQuizResultToBrowse,
    // Contact
    trackContactView, trackContactFormFocus, trackContactFormInput, trackContactFormBlur, trackContactFormValidate,
    trackContactFormSubmit, trackContactFormSuccess, trackContactFormError, trackContactMailtoClick, trackInquiryPrefillDetect,
    // Configurator
    trackConfiguratorView, trackConfiguratorOptionSelect, trackConfiguratorPreviewUpdate, trackConfiguratorSaveConfig,
    trackConfiguratorShareConfig, trackConfiguratorToInquiry,
    // Media
    trackMediaView, trackMediaFullScreen, trackMediaCarouselNav, trackDownloadStart, trackDownloadComplete,
    // Community
    trackCommunityView, trackCommunityChannelLink, trackCommunityEventView, trackCommunityEventRegister, trackShareClick,
    // Errors
    trackErrorPageLoad, trackErrorDataFetch, trackErrorFormValidation, trackErrorAnalyticsDebug,
    // Engagement
    trackScrollDepth, trackTimeOnPage, trackViewportResize, trackLinkClick,
    // Newsletter
    trackNewsletterSignupView, trackNewsletterSignupSubmit, trackNewsletterSignupSuccess,
    // Funnel
    trackFunnelExplore, trackFunnelConsider, trackFunnelCompare, trackFunnelInquire, trackFunnelAbandon,

    debugEnabled: DEBUG
  };
})();

// Expose as ZX.EventTracker for page scripts
window.ZX = window.ZX || {};
window.ZX.EventTracker = window.ZX.EventTracker || ZX.EventTracker;
