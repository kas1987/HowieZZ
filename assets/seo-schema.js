/* ============================================================
   ZELEX SEO Schema Markup Generator
   Structured data for Google Search, social sharing, etc.
   ============================================================ */

(function() {
  const Schema = {
    // Organization schema for header
    generateOrganizationSchema: function() {
      return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "ZELEX",
        "description": "Premium collectible dolls and customization platform",
        "url": "https://www.zelexdoll.com",
        "logo": "https://www.zelexdoll.com/assets/logo.svg",
        "sameAs": [
          "https://www.instagram.com/zelexdoll",
          "https://www.youtube.com/zelexofficial",
          "https://discord.gg/zelex"
        ],
        "contactPoint": {
          "@type": "ContactPoint",
          "contactType": "Customer Support",
          "email": "inquiries@zelexdoll.com",
          "url": "https://www.zelexdoll.com/contact.html"
        }
      };
    },

    // Community page schema
    generateCommunityPageSchema: function() {
      return {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "ZELEX Community Hub",
        "description": "Official ZELEX community hub for blogs, mags, Discord, and verified social channels",
        "url": "https://www.zelexdoll.com/community.html",
        "publisher": {
          "@type": "Organization",
          "name": "ZELEX",
          "logo": {
            "@type": "ImageObject",
            "url": "https://www.zelexdoll.com/assets/logo.svg"
          }
        },
        "potentialAction": {
          "@type": "CommunicateAction",
          "name": "Join Community",
          "target": "https://www.zelexdoll.com/community.html"
        }
      };
    },

    // Gallery page schema
    generateGalleryPageSchema: function(totalSubmissions, totalReviews) {
      return {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "ZELEX Community Gallery",
        "description": "Curated collection of verified ZELEX collector photos and reviews",
        "url": "https://www.zelexdoll.com/gallery.html",
        "mainEntity": {
          "@type": "Collection",
          "name": "Community Gallery Submissions",
          "numberOfItems": totalSubmissions || 0,
          "url": "https://www.zelexdoll.com/gallery.html",
          "isPartOf": {
            "@type": "WebSite",
            "name": "ZELEX Community",
            "url": "https://www.zelexdoll.com"
          }
        },
        "aggregateRating": {
          "@type": "AggregateRating",
          "ratingValue": "4.8",
          "reviewCount": totalReviews || 0,
          "worstRating": "1",
          "bestRating": "5"
        }
      };
    },

    // Individual gallery submission schema
    generateGalleryItemSchema: function(item) {
      if (!item) return null;

      return {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "name": item.title || "Gallery Submission",
        "description": item.description || "",
        "image": item.image_full_url || item.image_url || "",
        "creator": {
          "@type": "Person",
          "name": item.creator || "Community Member"
        },
        "datePublished": item.submitted_date || new Date().toISOString(),
        "dateModified": item.approved_date || item.submitted_date || new Date().toISOString(),
        "interactionStatistic": [
          {
            "@type": "InteractionCounter",
            "interactionType": "http://schema.org/LikeAction",
            "userInteractionCount": item.likes || 0
          }
        ],
        "keywords": (item.tags || []).join(", "),
        "about": {
          "@type": "Thing",
          "name": item.body_family || ""
        },
        "isPartOf": {
          "@type": "Collection",
          "name": "ZELEX Community Gallery",
          "url": "https://www.zelexdoll.com/gallery.html"
        }
      };
    },

    // Review/Aggregate rating schema
    generateReviewSchema: function(review) {
      if (!review) return null;

      return {
        "@context": "https://schema.org",
        "@type": "Review",
        "author": {
          "@type": "Person",
          "name": review.reviewer || "Verified Collector"
        },
        "datePublished": review.submitted_date || new Date().toISOString(),
        "description": review.body || review.title || "",
        "name": review.title || "",
        "reviewRating": {
          "@type": "Rating",
          "ratingValue": review.rating || 5,
          "worstRating": 1,
          "bestRating": 5
        },
        "isBasedOn": {
          "@type": "Product",
          "name": review.body_family || "ZELEX Product"
        }
      };
    },

    // Event schema for community events
    generateEventSchema: function(event) {
      if (!event) return null;

      // Parse date and time
      const dateStart = event.date || "2026-07-05";
      const timeStart = event.time_start || "14:00Z";
      const timeEnd = event.time_end || "15:00Z";

      // Format for schema.org (ISO 8601)
      const startDateTime = `${dateStart.replace(/-/g, "")}T${timeStart.replace(/:/g, "")}`;
      const endDateTime = `${dateStart.replace(/-/g, "")}T${timeEnd.replace(/:/g, "")}`;

      return {
        "@context": "https://schema.org",
        "@type": "Event",
        "name": event.title || "",
        "description": event.description || event.summary || "",
        "startDate": startDateTime,
        "endDate": endDateTime,
        "eventStatus": "https://schema.org/EventScheduled",
        "eventAttendanceMode": event.mode === "Virtual meetup" || event.mode === "Discord"
          ? "https://schema.org/OnlineEventAttendanceMode"
          : event.mode === "Regional Meetup" || event.mode === "In-person"
          ? "https://schema.org/OfflineEventAttendanceMode"
          : "https://schema.org/MixedEventAttendanceMode",
        "location": {
          "@type": "Place",
          "name": event.location || "ZELEX Community"
        },
        "organizer": {
          "@type": "Organization",
          "name": "ZELEX",
          "url": "https://www.zelexdoll.com"
        },
        "offers": {
          "@type": "Offer",
          "url": event.ctaHref || "https://www.zelexdoll.com/community-events.html",
          "price": "0",
          "priceCurrency": "USD",
          "availability": "https://schema.org/PreOrder",
          "validFrom": new Date().toISOString()
        }
      };
    },

    // Breadcrumb schema
    generateBreadcrumbSchema: function(path) {
      const pathArray = path || ['Atlas', 'Community', 'Gallery'];

      return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": pathArray.map((item, index) => ({
          "@type": "ListItem",
          "position": index + 1,
          "name": item,
          "item": this.getBreadcrumbUrl(index)
        }))
      };
    },

    getBreadcrumbUrl: function(index) {
      const urls = [
        "https://www.zelexdoll.com/index.html",
        "https://www.zelexdoll.com/community.html",
        "https://www.zelexdoll.com/gallery.html",
        "https://www.zelexdoll.com/community-events.html"
      ];
      return urls[index] || "https://www.zelexdoll.com";
    },

    // FAQPage schema for community guidelines
    generateFAQSchema: function(faqs) {
      if (!faqs || !Array.isArray(faqs)) return null;

      return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": faqs.map(item => ({
          "@type": "Question",
          "name": item.question || "",
          "acceptedAnswer": {
            "@type": "Answer",
            "text": item.answer || ""
          }
        }))
      };
    },

    // Inject schema into page head
    injectSchema: function(schema) {
      if (!schema) return false;

      try {
        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(schema, null, 2);
        document.head.appendChild(script);
        return true;
      } catch (e) {
        console.error('Schema injection failed:', e);
        return false;
      }
    },

    // Inject multiple schemas
    injectSchemas: function(schemas) {
      if (!Array.isArray(schemas)) schemas = [schemas];
      schemas.forEach(schema => this.injectSchema(schema));
    },

    // Auto-inject for known pages
    autoInject: function() {
      const pathname = window.location.pathname.toLowerCase();

      if (pathname.includes('community.html')) {
        this.injectSchemas([
          this.generateOrganizationSchema(),
          this.generateCommunityPageSchema(),
          this.generateBreadcrumbSchema(['Atlas', 'Community'])
        ]);
      } else if (pathname.includes('gallery.html')) {
        this.injectSchemas([
          this.generateOrganizationSchema(),
          this.generateGalleryPageSchema(),
          this.generateBreadcrumbSchema(['Atlas', 'Community', 'Gallery'])
        ]);
      } else if (pathname.includes('community-events.html')) {
        this.injectSchemas([
          this.generateOrganizationSchema(),
          this.generateBreadcrumbSchema(['Atlas', 'Community', 'Events'])
        ]);
      }
    }
  };

  // Expose to global scope
  if (typeof window !== 'undefined') {
    window.SEOSchema = Schema;
  }

  // Auto-inject on DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      Schema.autoInject();
    });
  } else {
    Schema.autoInject();
  }
})();
