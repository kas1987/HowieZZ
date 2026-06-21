/* ============================================================
   ZELEX Gallery Widget
   Community submission & review carousel
   ============================================================ */

(function() {
  const GW = {
    SUBMISSION_QUEUE_KEY: 'zx_gallery_submissions',
    REVIEW_QUEUE_KEY: 'zx_gallery_reviews',

    // Store submission draft locally
    saveSubmissionDraft: function(data) {
      try {
        localStorage.setItem(GW.SUBMISSION_QUEUE_KEY, JSON.stringify({
          timestamp: Date.now(),
          data: data
        }));
        return true;
      } catch (e) {
        console.error('Gallery: could not save draft', e);
        return false;
      }
    },

    // Load submission draft
    getSubmissionDraft: function() {
      try {
        const stored = localStorage.getItem(GW.SUBMISSION_QUEUE_KEY);
        if (!stored) return null;
        const parsed = JSON.parse(stored);
        // Discard drafts older than 7 days
        if (Date.now() - parsed.timestamp > 7 * 24 * 60 * 60 * 1000) {
          localStorage.removeItem(GW.SUBMISSION_QUEUE_KEY);
          return null;
        }
        return parsed.data;
      } catch (e) {
        console.error('Gallery: could not load draft', e);
        return null;
      }
    },

    // Clear submission draft
    clearSubmissionDraft: function() {
      try {
        localStorage.removeItem(GW.SUBMISSION_QUEUE_KEY);
        return true;
      } catch (e) {
        console.error('Gallery: could not clear draft', e);
        return false;
      }
    },

    // Validate submission
    validateSubmission: function(data) {
      const errors = [];
      if (!data.title || !data.title.trim()) errors.push('Title is required');
      if (!data.description || !data.description.trim()) errors.push('Description is required');
      if (!data.creator || !data.creator.trim()) errors.push('Creator name is required');
      if (!data.body_family) errors.push('Body family selection is required');
      if (!data.image_file && !data.image_url) errors.push('Image is required');
      return { valid: errors.length === 0, errors };
    },

    // Validate review
    validateReview: function(data) {
      const errors = [];
      if (!data.title || !data.title.trim()) errors.push('Review title is required');
      if (!data.body || !data.body.trim()) errors.push('Review text is required');
      if (!data.rating || data.rating < 1 || data.rating > 5) errors.push('Rating must be 1-5 stars');
      if (!data.body_family) errors.push('Body family is required');
      return { valid: errors.length === 0, errors };
    },

    // Submit to backend (via contact form endpoint)
    submitToBackend: function(payload, endpoint) {
      if (!endpoint) {
        console.warn('Gallery: no endpoint configured, would submit:', payload);
        return Promise.resolve({ success: true, message: 'Submission queued for moderation' });
      }

      return fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      })
        .then(r => r.json())
        .catch(e => {
          console.error('Gallery: submission error', e);
          throw new Error('Could not submit; please try again or contact support');
        });
    },

    // Format star rating display
    formatRating: function(rating) {
      return '★'.repeat(rating) + '☆'.repeat(5 - rating);
    },

    // Parse and render featured reviews
    renderReviewCarousel: function(reviews, containerId) {
      const container = document.getElementById(containerId);
      if (!container || !Array.isArray(reviews)) return;

      const featured = reviews.filter(r => r.featured || r.rating >= 4);
      if (featured.length === 0) return;

      let currentIndex = 0;

      container.innerHTML = featured
        .map((r, i) => `
          <div class="review-card ${i === 0 ? 'active' : ''}" data-index="${i}">
            <div class="review-stars">${GW.formatRating(r.rating)}</div>
            <h4 class="review-title">${r.title || ''}</h4>
            <p class="review-text">${r.body || ''}</p>
            <div class="review-footer">
              <span class="review-author">${r.reviewer || 'Verified Collector'}</span>
              <span class="review-meta">${r.body_family || ''}</span>
            </div>
          </div>
        `)
        .join('');

      // Add navigation dots
      const navContainer = document.createElement('div');
      navContainer.className = 'review-nav-dots';
      featured.forEach((_, i) => {
        const dot = document.createElement('button');
        dot.className = `nav-dot ${i === 0 ? 'active' : ''}`;
        dot.setAttribute('aria-label', `Review ${i + 1}`);
        dot.addEventListener('click', () => {
          currentIndex = i;
          GW.updateCarouselIndex(container, currentIndex, featured.length);
        });
        navContainer.appendChild(dot);
      });
      container.parentNode.insertBefore(navContainer, container.nextSibling);

      // Auto-rotate (optional)
      setInterval(() => {
        currentIndex = (currentIndex + 1) % featured.length;
        GW.updateCarouselIndex(container, currentIndex, featured.length);
      }, 6000);
    },

    updateCarouselIndex: function(container, index, total) {
      container.querySelectorAll('.review-card').forEach((card, i) => {
        card.classList.toggle('active', i === index);
      });
      container.parentNode.querySelectorAll('.nav-dot').forEach((dot, i) => {
        dot.classList.toggle('active', i === index);
      });
    },

    // Track gallery engagement
    trackGalleryEvent: function(eventName, metadata) {
      if (typeof ZX !== 'undefined' && ZX.track) {
        ZX.track(eventName, Object.assign({ context: 'gallery' }, metadata));
      }
    }
  };

  // Expose to global scope
  if (typeof window !== 'undefined') {
    window.GalleryWidget = GW;
  }

  // Auto-initialize if embedded
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      // Reserved for future auto-init if needed
    });
  }
})();
