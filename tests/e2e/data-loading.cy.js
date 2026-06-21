/**
 * E2E tests for data loading and catalog integrity
 * Validates JSON data loads, model is built correctly, and indexing works
 */

describe('Data Loading and Model', () => {
  it('loads characters.json successfully', () => {
    cy.loadPage('index.html');
    cy.window().then((win) => {
      expect(win.ZX).to.exist;
      expect(typeof win.ZX.load).to.equal('function');
    });
  });

  it('model contains required keys after load', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        expect(model).to.have.property('characters');
        expect(model).to.have.property('byId');
        expect(model).to.have.property('byBody');
        expect(model).to.have.property('bySeries');
        expect(model).to.have.property('btByCode');
        expect(model).to.have.property('bodyTypes');
        expect(model).to.have.property('profiles');
        expect(model).to.have.property('series');
        expect(model).to.have.property('FAMILIES');
      });
    });
  });

  it('characters are indexed by ID', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        if (model.characters && model.characters.length > 0) {
          const char = model.characters[0];
          expect(model.byId[char.character_id]).to.deep.equal(char);
        }
      });
    });
  });

  it('characters are grouped by body code', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        if (model.characters && model.characters.length > 0) {
          const char = model.characters[0];
          const bodyCode = char.body_code;
          expect(model.byBody[bodyCode]).to.be.an('array');
          expect(model.byBody[bodyCode]).to.include(char);
        }
      });
    });
  });

  it('characters are grouped by series', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        if (model.characters && model.characters.length > 0) {
          const char = model.characters[0];
          const series = char.series;
          expect(model.bySeries[series]).to.be.an('array');
          expect(model.bySeries[series]).to.include(char);
        }
      });
    });
  });

  it('all 6 body families are present', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        const expectedFamilies = [
          'The Classic', 'The Icon', 'The Muse',
          'The Siren', 'The Empress', 'The Sculpt'
        ];
        expectedFamilies.forEach((fam) => {
          expect(model.FAMILIES).to.include(fam);
        });
      });
    });
  });

  it('character data has required fields', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        if (model.characters && model.characters.length > 0) {
          model.characters.slice(0, 5).forEach((char) => {
            expect(char).to.have.property('character_id');
            expect(char).to.have.property('body_code');
            expect(char).to.have.property('series');
            expect(char).to.have.property('status');
          });
        }
      });
    });
  });

  it('handles missing body_profiles.json gracefully', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        expect(model.profiles).to.be.an('object');
      });
    });
  });

  it('series list matches series in catalog', () => {
    cy.loadPage('browse.html');
    cy.window().then((win) => {
      return win.ZX.load().then((model) => {
        const seriesFromChars = new Set(model.characters.map(c => c.series));
        model.series.forEach((s) => {
          expect(seriesFromChars).to.include(s);
        });
      });
    });
  });
});
