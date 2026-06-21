/**
 * Unit tests for quiz recommendation engine
 * Run: npm test -- tests/recommend.test.js
 */

import { describe, it, expect, beforeEach } from '@jest/globals';
import {
  recommend,
  scoreAnswers,
  rankFamiliesAndResolve,
  buildReasoning
} from '../api/recommend.js';

// Mock catalog data
const MOCK_CATALOG = {
  families: [
    {
      name: "The Classic",
      whr: [0.68, 0.72],
      bwr: [1.4, 1.5],
      silhouette: "Timeless hourglass",
      premium: "+20%"
    },
    {
      name: "The Muse",
      whr: [0.65, 0.7],
      bwr: [1.3, 1.4],
      silhouette: "Tall, hip-dominant",
      premium: "+25%"
    },
    {
      name: "The Siren",
      whr: [0.55, 0.6],
      bwr: [1.6, 1.75],
      silhouette: "Bust-dominant fantasy",
      premium: "+35%"
    },
    {
      name: "The Icon",
      whr: [0.6, 0.65],
      bwr: [1.5, 1.6],
      silhouette: "Glamour model",
      premium: "+30%"
    },
    {
      name: "The Empress",
      whr: [0.58, 0.64],
      bwr: [1.55, 1.65],
      silhouette: "Maximum plush",
      premium: "+40%"
    },
    {
      name: "The Sculpt",
      whr: [0.65, 0.68],
      bwr: [1.45, 1.55],
      silhouette: "Muscular definition",
      premium: "+30%"
    }
  ],
  characters: [
    {
      character_id: "test-classic-01",
      status: "live",
      body_code: "TC161",
      series: "TestSeries",
      body: {
        family: "The Classic",
        WHR: 0.70,
        BWR: 1.45,
        height_cm: 161,
        cup: "D"
      },
      persona: { name: "Test Classic" },
      photoshoot: { hero: "test.jpg" }
    },
    {
      character_id: "test-muse-01",
      status: "live",
      body_code: "TM168",
      series: "TestSeries",
      body: {
        family: "The Muse",
        WHR: 0.67,
        BWR: 1.35,
        height_cm: 168,
        cup: "C"
      },
      persona: { name: "Test Muse" },
      photoshoot: { hero: "test.jpg" }
    },
    {
      character_id: "test-siren-01",
      status: "live",
      body_code: "TS156",
      series: "TestSeries",
      body: {
        family: "The Siren",
        WHR: 0.58,
        BWR: 1.68,
        height_cm: 156,
        cup: "F"
      },
      persona: { name: "Test Siren" },
      photoshoot: { hero: "test.jpg" }
    }
  ]
};

describe('recommend()', () => {
  it('should score single-answer quiz correctly', async () => {
    const answers = [
      {
        weights: { "The Muse": 2, "The Icon": 1 },
        whr: 0.3,
        bwr: -0.2
      }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.winner).toBe("The Muse");
    expect(result.sourceFam).toBe("The Muse");
    expect(result.matches.length).toBeGreaterThan(0);
    expect(result.measurement.whrLean).toBe(0.3);
    expect(result.measurement.bwrLean).toBe(-0.2);
  });

  it('should accumulate scores across multiple answers', async () => {
    const answers = [
      {
        weights: { "The Classic": 2, "The Muse": 1 },
        whr: -0.2,
        bwr: 0.1
      },
      {
        weights: { "The Classic": 3 },
        whr: -0.1,
        bwr: 0.0
      },
      {
        weights: { "The Classic": 1, "The Icon": 2 },
        whr: 0.0,
        bwr: 0.5
      }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.winner).toBe("The Classic");
    expect(result.topFamilies[0].family).toBe("The Classic");
    expect(result.topFamilies[0].pct).toBeGreaterThan(50); // Should dominate
  });

  it('should return top 3 families ranked by score', async () => {
    const answers = [
      { weights: { "The Muse": 3, "The Icon": 2, "The Classic": 1 }, whr: 0, bwr: 0 },
      { weights: { "The Muse": 2, "The Icon": 1 }, whr: 0, bwr: 0 },
      { weights: { "The Muse": 1, "The Icon": 3 }, whr: 0, bwr: 0 }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.topFamilies.length).toBe(3);
    expect(result.topFamilies[0].rank).toBe(1);
    expect(result.topFamilies[1].rank).toBe(2);
    expect(result.topFamilies[2].rank).toBe(3);
    expect(result.topFamilies[0].pct).toBeGreaterThanOrEqual(result.topFamilies[1].pct);
  });

  it('should return up to 4 character matches', async () => {
    const answers = [
      { weights: { "The Muse": 3 }, whr: 0.3, bwr: -0.2 }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.matches.length).toBeLessThanOrEqual(4);
    expect(result.matches.every(m => m.family === "The Muse" || m.family === null)).toBe(true);
  });

  it('should include reasoning with measurement language', async () => {
    const answers = [
      { weights: { "The Siren": 3 }, whr: -0.4, bwr: 0.8 }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.measurement.reasoning).toBeDefined();
    expect(result.measurement.reasoning.whrDir).toBeDefined();
    expect(result.measurement.reasoning.bwrDir).toBeDefined();
    expect(result.measurement.reasoning.ranges).toBeDefined();
    expect(result.measurement.reasoning.confidence).toBe("near");
  });

  it('should set variant in result', async () => {
    const answers = [{ weights: { "The Classic": 1 }, whr: 0, bwr: 0 }];

    const controlResult = await recommend(answers, MOCK_CATALOG, { abVariant: 'control' });
    const treatmentResult = await recommend(answers, MOCK_CATALOG, { abVariant: 'treatment' });

    expect(controlResult.variant).toBe('control');
    expect(treatmentResult.variant).toBe('treatment');
  });

  it('should throw on missing catalog', async () => {
    const answers = [{ weights: { "The Classic": 1 }, whr: 0, bwr: 0 }];

    await expect(recommend(answers, null)).rejects.toThrow('Catalog data required');
    await expect(recommend(answers, {})).rejects.toThrow('Catalog data required');
  });

  it('should throw on missing answers', async () => {
    await expect(recommend(null, MOCK_CATALOG)).rejects.toThrow('Answers array required');
    await expect(recommend([], MOCK_CATALOG)).toResolve(); // Empty array is valid
  });
});

describe('scoreAnswers()', () => {
  it('should initialize scores to 0', () => {
    const families = ["The Classic", "The Muse"];
    const answers = [];

    const { scores } = scoreAnswers(answers, families);

    expect(scores["The Classic"]).toBe(0);
    expect(scores["The Muse"]).toBe(0);
  });

  it('should accumulate weights correctly', () => {
    const families = ["The Classic", "The Muse"];
    const answers = [
      { weights: { "The Classic": 2, "The Muse": 1 } },
      { weights: { "The Classic": 1, "The Muse": 3 } }
    ];

    const { scores } = scoreAnswers(answers, families);

    expect(scores["The Classic"]).toBe(3);
    expect(scores["The Muse"]).toBe(4);
  });

  it('should average measurement leans', () => {
    const families = ["The Classic"];
    const answers = [
      { whr: 0.2, bwr: 0.4 },
      { whr: 0.4, bwr: 0.2 },
      { whr: 0.2, bwr: 0.2 }
    ];

    const { avgWhr, avgBwr } = scoreAnswers(answers, families);

    expect(avgWhr).toBe((0.2 + 0.4 + 0.2) / 3);
    expect(avgBwr).toBe((0.4 + 0.2 + 0.2) / 3);
  });

  it('should handle missing measurements', () => {
    const families = ["The Classic"];
    const answers = [
      { whr: 0.2 },         // missing bwr
      { bwr: 0.4 },         // missing whr
      { whr: 0.2, bwr: 0.2 }
    ];

    const { avgWhr, avgBwr } = scoreAnswers(answers, families);

    expect(avgWhr).toBe((0.2 + 0.2) / 2); // Only 2 whr values
    expect(avgBwr).toBe((0.4 + 0.2) / 2); // Only 2 bwr values
  });
});

describe('rankFamiliesAndResolve()', () => {
  it('should rank families by score', () => {
    const scores = {
      "The Classic": 5,
      "The Muse": 8,
      "The Siren": 3
    };
    const families = ["The Classic", "The Muse", "The Siren"];

    const result = rankFamiliesAndResolve(scores, families, MOCK_CATALOG, "The Muse");

    expect(result.ranked[0]).toBe("The Muse");
    expect(result.ranked[1]).toBe("The Classic");
    expect(result.ranked[2]).toBe("The Siren");
  });

  it('should resolve to live family when expressed is in-dev', () => {
    const catalog = {
      ...MOCK_CATALOG,
      characters: MOCK_CATALOG.characters.filter(c => c.body.family !== "The Sculpt")
    };
    const scores = { "The Sculpt": 5, "The Muse": 3, "The Classic": 2 };
    const families = ["The Sculpt", "The Muse", "The Classic"];

    const result = rankFamiliesAndResolve(scores, families, catalog, "The Sculpt");

    expect(result.sourceFam).not.toBe("The Sculpt");
    expect(result.isInDev("The Sculpt")).toBe(true);
  });

  it('should find nearest active family by measurement distance', () => {
    const scores = { "The Sculpt": 10 };
    const families = ["The Sculpt"];

    const result = rankFamiliesAndResolve(scores, families, MOCK_CATALOG, "The Sculpt");

    // Sculpt is in-dev (no live chars), should fallback
    const source = result.sourceFam;
    expect(result.isInDev("The Sculpt")).toBe(true);
    // Should pick a live family
    expect(["The Classic", "The Muse", "The Siren"].includes(source)).toBe(true);
  });
});

describe('buildReasoning()', () => {
  it('should describe WHR direction correctly', () => {
    const whrHigh = buildReasoning("The Classic", MOCK_CATALOG.families, 0.3, 0);
    expect(whrHigh.whrDir).toContain("higher");

    const whrLow = buildReasoning("The Siren", MOCK_CATALOG.families, -0.3, 0);
    expect(whrLow.whrDir).toContain("lower");

    const whrMid = buildReasoning("The Muse", MOCK_CATALOG.families, 0.05, 0);
    expect(whrMid.whrDir).toContain("balanced");
  });

  it('should describe BWR direction correctly', () => {
    const bwrHigh = buildReasoning("The Siren", MOCK_CATALOG.families, 0, 0.5);
    expect(bwrHigh.bwrDir).toContain("bust-forward");

    const bwrLow = buildReasoning("The Muse", MOCK_CATALOG.families, 0, -0.5);
    expect(bwrLow.bwrDir).toContain("restrained");

    const bwrMid = buildReasoning("The Classic", MOCK_CATALOG.families, 0, 0.05);
    expect(bwrMid.bwrDir).toContain("moderate");
  });

  it('should include family measurement ranges', () => {
    const reasoning = buildReasoning("The Classic", MOCK_CATALOG.families, 0, 0);

    expect(reasoning.ranges).toContain("0.68");
    expect(reasoning.ranges).toContain("0.72");
    expect(reasoning.ranges).toContain("1.4");
    expect(reasoning.ranges).toContain("1.5");
  });

  it('should set confidence to "near"', () => {
    const reasoning = buildReasoning("The Muse", MOCK_CATALOG.families, 0.2, -0.3);

    expect(reasoning.confidence).toBe("near");
  });
});

describe('A/B Testing', () => {
  it('control variant should not modify scores', async () => {
    const answers = [
      { weights: { "The Classic": 2, "The Muse": 1 }, whr: 0.3, bwr: -0.2 }
    ];

    const result = await recommend(answers, MOCK_CATALOG, { abVariant: 'control' });

    expect(result.variant).toBe('control');
    expect(result.topFamilies[0].family).toBe("The Classic"); // No boost
  });

  it('treatment variant should possibly modify scores', async () => {
    const answers = [
      {
        weights: { "The Siren": 3, "The Classic": 1 },
        whr: -0.35,  // Aligns well with Siren's center
        bwr: 0.70    // Aligns well with Siren's center
      }
    ];

    const controlResult = await recommend(answers, MOCK_CATALOG, { abVariant: 'control' });
    const treatmentResult = await recommend(answers, MOCK_CATALOG, { abVariant: 'treatment' });

    // Treatment should have same or better confidence
    expect(treatmentResult.variant).toBe('treatment');
    // Score distribution might differ due to alignment boost
    expect(treatmentResult.topFamilies).toBeDefined();
  });
});

describe('Edge Cases', () => {
  it('should handle empty answers array', async () => {
    const result = await recommend([], MOCK_CATALOG);

    expect(result).toBeDefined();
    expect(result.matches).toBeDefined();
  });

  it('should handle answers with no weights', async () => {
    const answers = [
      { whr: 0.2, bwr: 0.1 },
      { whr: -0.1, bwr: 0.3 }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result).toBeDefined();
  });

  it('should handle catalog with no live characters', async () => {
    const emptyCatalog = {
      ...MOCK_CATALOG,
      characters: []
    };

    const answers = [{ weights: { "The Classic": 1 }, whr: 0, bwr: 0 }];

    const result = await recommend(answers, emptyCatalog);

    expect(result.matches.length).toBe(0);
  });

  it('should handle very high/low measurement leans', async () => {
    const answers = [
      { weights: { "The Siren": 3 }, whr: -1.0, bwr: 2.0 }
    ];

    const result = await recommend(answers, MOCK_CATALOG);

    expect(result.measurement.whrLean).toBe(-1.0);
    expect(result.measurement.bwrLean).toBe(2.0);
    expect(result.measurement.reasoning).toBeDefined();
  });
});
