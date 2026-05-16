/**
 * Lighthouse CI configuration.
 * Copy to project root as lighthouserc.js and adjust thresholds.
 * Run: npx lhci autorun
 */
module.exports = {
  ci: {
    collect: {
      numberOfRuns: 3,
      // Set your URL(s) — can be localhost for pre-deploy checks
      url: ["http://localhost:3000", "http://localhost:3000/about"],
      settings: {
        // Throttle to simulate mobile 4G
        throttlingMethod: "simulate",
        throttling: {
          rttMs: 40,
          throughputKbps: 10 * 1024,
          cpuSlowdownMultiplier: 4,
        },
        // Mobile viewport
        emulatedFormFactor: "mobile",
        screenEmulation: {
          mobile: true,
          width: 412,
          height: 823,
          deviceScaleFactor: 1.75,
        },
      },
    },
    assert: {
      assertions: {
        // Core Web Vitals
        "largest-contentful-paint": ["error", { maxNumericValue: 2500 }],
        "cumulative-layout-shift": ["error", { maxNumericValue: 0.1 }],
        "total-blocking-time": ["warn", { maxNumericValue: 200 }],
        "first-contentful-paint": ["warn", { maxNumericValue: 1800 }],
        "interactive": ["warn", { maxNumericValue: 3800 }],

        // Category scores (0–1)
        "categories:performance": ["warn", { minScore: 0.9 }],
        "categories:accessibility": ["error", { minScore: 0.9 }],
        "categories:best-practices": ["warn", { minScore: 0.9 }],
        "categories:seo": ["warn", { minScore: 0.9 }],

        // Image optimization
        "uses-optimized-images": ["warn", { maxLength: 0 }],
        "uses-webp-images": ["warn", { maxLength: 0 }],
        "uses-responsive-images": ["warn", { maxLength: 0 }],

        // JavaScript
        "unused-javascript": ["warn", { maxLength: 0 }],
        "render-blocking-resources": ["warn", { maxLength: 0 }],
        "unused-css-rules": ["warn", { maxLength: 0 }],
      },
    },
    upload: {
      // Upload to temporary public storage (no account needed)
      // Switch to target: "lhci" and add serverBaseUrl for self-hosted
      target: "temporary-public-storage",
    },
  },
};
