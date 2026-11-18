import { describe, it, expect } from 'vitest';
import { countByStatus, completionRate } from './tasks';

/**
 * Tests des fonctions utilitaires (tasks.ts)
 *
 * Ces tests sont écrits en JavaScript : même structure qu'en Python avec pytest :
 *
 *   Python (pytest)                       JavaScript (Vitest)
 *   from tasks import completionRate      import { completionRate } from './tasks';
 *   class TestCompletionRate:             describe('completionRate', () => { ... });
 *   def test_xxx():                       it('xxx', () => { ... });
 *   tasks = [...]                         const tasks = [...];
 *   assert resultat == 3                  expect(resultat).toBe(3);
 *   assert resultat == {"a": 1}           expect(resultat).toEqual({ a: 1 });
 *
 * () => { ... } est une fonction sans nom : l'équivalent d'un def.
 *
 * toBe    → compare une valeur simple (nombre, texte, booléen)
 * toEqual → compare le contenu d'un objet ou d'un tableau
 */

// =============================================================================
// PARTIE 1 : TESTS EXEMPLES (lisez-les !)
// =============================================================================

describe('countByStatus', () => {
  it('compte les tâches de chaque statut', () => {
    // ARRANGE : préparer une liste de tâches
    const tasks = [
      { status: 'todo' },
      { status: 'todo' },
      { status: 'done' },
    ];

    // ACT : appeler la fonction à tester
    const counts = countByStatus(tasks);

    // ASSERT : vérifier le résultat
    expect(counts).toEqual({ todo: 2, in_progress: 0, done: 1 });
  });

  it('renvoie des zéros pour une liste vide', () => {
    const counts = countByStatus([]);

    expect(counts).toEqual({ todo: 0, in_progress: 0, done: 0 });
  });
});

// =============================================================================
// PARTIE 2 : À VOUS ! (TP 1 - Exercice 4)
// =============================================================================
//
// Écrivez les 3 tests de completionRate().
// Pour chaque test : supprimez la ligne `throw new Error(...)`,
// puis écrivez ARRANGE / ACT / ASSERT comme dans les exemples ci-dessus.
//
// Lancer les tests : npm test

describe('completionRate', () => {
  it('calcule le pourcentage de tâches terminées', () => {
    // ARRANGE : 4 tâches, dont 2 avec le statut 'done'
    const tasks = [
      { status: 'done' },
      { status: 'done' },
      { status: 'todo' },
      { status: 'in_progress' },
    ];

    // ACT : appeler la fonction à tester
    const rate = completionRate(tasks);

    // ASSERT : 2 tâches terminées sur 4 → 50
    expect(rate).toBe(50);
  });

  it('renvoie 100 quand toutes les tâches sont terminées', () => {
    // ARRANGE : 2 tâches, toutes les deux 'done'
    const tasks = [
      { status: 'done' },
      { status: 'done' },
    ];

    // ACT : appeler completionRate(tasks)
    const rate = completionRate(tasks);

    // ASSERT : 2 sur 2 → 100
    expect(rate).toBe(100);
  });

  it('renvoie 0 pour une liste vide', () => {
    // ARRANGE : une liste vide
    const tasks = [];

    // ACT : appeler completionRate([])
    const rate = completionRate(tasks);

    // ASSERT : cas limite, pas de division par zéro → 0
    expect(rate).toBe(0);
  });
});
