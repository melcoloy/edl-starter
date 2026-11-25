"""
Tests API TaskFlow - TP 1

Apprenez en faisant ! Ce fichier vous montre comment écrire des tests, puis vous en écrirez de similaires.

Structure de chaque test :
1. ARRANGE - Préparer les données de test
2. ACT - Faire la requête API
3. ASSERT - Vérifier la réponse
"""

import pytest


# =============================================================================
# PARTIE 1 : TESTS EXEMPLES (Apprenez de ceux-ci !)
# =============================================================================

def test_root_endpoint(client):
    """
    EXEMPLE : Tester un point de terminaison GET simple.

    Ce test vous montre le pattern de base :
    1. Faire une requête avec client.get()
    2. Vérifier le code de statut
    3. Vérifier les données de la réponse
    """
    # ACT : Faire une requête GET
    response = client.get("/")

    # ASSERT : Vérifier la réponse
    assert response.status_code == 200
    assert "Welcome to TaskFlow API" in response.json()["message"]


def test_health_check(client):
    
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "BROKEN"  # ❌ Faux exprès !


def test_create_task(client):
    """
    EXEMPLE : Tester un point de terminaison POST (création de données).

    Pattern pour les requêtes POST :
    1. Préparer les données comme un dictionnaire Python
    2. Les envoyer avec client.post()
    3. Vérifier le code de statut (201 = Créé)
    4. Vérifier les données retournées
    """
    # ARRANGE : Préparer les données
    new_task = {
        "title": "Acheter des courses",
        "description": "Lait, œufs, pain"
    }

    # ACT : Envoyer la requête POST
    response = client.post("/tasks", json=new_task)

    # ASSERT : Vérifier la réponse
    assert response.status_code == 201  # 201 = Créé

    task = response.json()
    assert task["title"] == "Acheter des courses"
    assert task["description"] == "Lait, œufs, pain"
    assert task["status"] == "todo"  # Valeur par défaut
    assert "id" in task  # Le serveur génère un ID


def test_list_tasks(client):
    """
    EXEMPLE : Tester GET avec préparation de données.

    Parfois vous devez créer des données d'abord, puis tester leur listage.
    """
    # ARRANGE : Créer quelques tâches d'abord
    client.post("/tasks", json={"title": "Tâche 1"})
    client.post("/tasks", json={"title": "Tâche 2"})

    # ACT : Obtenir la liste des tâches
    response = client.get("/tasks")

    # ASSERT : Vérifier qu'on a bien les deux tâches
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2


def test_get_task_by_id(client):
    """
    EXEMPLE : Tester GET pour une ressource spécifique.

    Pattern :
    1. Créer une tâche d'abord
    2. Obtenir son ID depuis la réponse
    3. Utiliser cet ID pour récupérer la tâche
    """
    # ARRANGE : Créer une tâche
    create_response = client.post("/tasks", json={"title": "Trouve-moi"})
    task_id = create_response.json()["id"]

    # ACT : Obtenir la tâche spécifique
    response = client.get(f"/tasks/{task_id}")

    # ASSERT : Vérifier qu'on a la bonne tâche
    assert response.status_code == 200
    assert response.json()["title"] == "Trouve-moi"


# =============================================================================
# PARTIE 2 : À VOUS ! (Exercices 1 et 2)
# =============================================================================
#
# Écrivez d'abord ces tests : ils échouent, car delete_task() et update_task()
# ne sont pas encore écrites dans src/app.py. Puis écrivez ces fonctions
# jusqu'à ce que les tests passent.
#
# Pour chaque test : supprimez la ligne pytest.fail(...), puis écrivez
# ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

# --- Exercice 1 : supprimer une tâche ---

def test_delete_task(client):
    """Supprimer une tâche existante renvoie 204, puis la tâche n'existe plus (GET → 404)."""
    # ARRANGE : créer une tâche à supprimer
    create_response = client.post("/tasks", json={"title": "À supprimer"})
    task_id = create_response.json()["id"]

    # ACT : supprimer la tâche
    response = client.delete(f"/tasks/{task_id}")

    # ASSERT : 204 = pas de contenu la tâche n'existe plus
    assert response.status_code == 204
    assert client.get(f"/tasks/{task_id}").status_code == 404


def test_delete_nonexistent_task(client):
    """Supprimer une tâche qui n'existe pas renvoie 404."""
    # ARRANGE : créer une tâche, puis la supprimer, pour obtenir un ID dont on
    # est sûr qu'il n'existe plus
    create_response = client.post("/tasks", json={"title": "Temporaire"})
    task_id = create_response.json()["id"]
    client.delete(f"/tasks/{task_id}")

    # ACT : supprimer cette tâche une deuxième fois
    response = client.delete(f"/tasks/{task_id}")

    # ASSERT : 404 = Non Trouvé
    assert response.status_code == 404


# --- Exercice 2 : modifier une tâche ---

def test_update_task_title(client):
    """Modifier le titre d'une tâche renvoie 200 et la tâche avec le nouveau titre."""
    # arrange : préparation de la tâche à modifier
    create_response = client.post("/tasks", json={"title": "Ancien titre"})
    task_id = create_response.json()["id"]

    # act : modification du titre
    response = client.put(f"/tasks/{task_id}", json={"title": "Nouveau titre"})

    # assert : vérification : 200 et le titre est bien modifié
    assert response.status_code == 200
    assert response.json()["title"] == "Nouveau titre"


def test_update_only_changes_sent_fields(client):
    """Créez une tâche avec un titre, une description et une priorité,
    puis envoyez seulement {"status": "done"} : le statut change,
    mais le titre, la description et la priorité restent identiques."""
    # arrange : tache initiale avec titre, description et priorité
    create_response = client.post("/tasks", json={
        "title": "Tâche à modifier",
        "description": "Description initiale",
        "priority": "high"
    })
    task_id = create_response.json()["id"]

    # act : envoie de {"status": "done"} pour mise à jour
    response = client.put(f"/tasks/{task_id}", json={"status": "done"})

    # assert : vérification que seul le statut a changé
    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["status"] == "done"
    assert updated_task["title"] == "Tâche à modifier"
    assert updated_task["description"] == "Description initiale"
    assert updated_task["priority"] == "high"


def test_update_nonexistent_task(client):
    """Modifier une tâche qui n'existe pas renvoie 404."""
    # arrange : ressemble à test_delete_nonexistent_task : créer une tâche, la supprimer, pour avoir un ID inexistant
    create_response = client.post("/tasks", json={"title": "Temporaire"})
    task_id = create_response.json()["id"]
    client.delete(f"/tasks/{task_id}")

    # act : tentative de modification de cette tâche inexistante
    response = client.put(f"/tasks/{task_id}", json={"title": "i guess we'll never know"})

    # assert : vérification tache inexistante renvoie 404
    assert response.status_code == 404


# =============================================================================
# PARTIE 3 : À VOUS ! (Exercice 3)
# =============================================================================
#
# Écrivez ces tests. Pour chacun : supprimez la ligne pytest.fail(...),
# puis écrivez ARRANGE / ACT / ASSERT. La docstring dit ce qu'il faut vérifier.

def test_create_task_with_empty_title(client):
    """Créer une tâche avec un titre vide ("") est refusé : 422."""
    # arrange : préparation de la tâche avec un titre vide
    task_vide = {"title": ""}

    # act : tentative de création de la tâche
    response = client.post("/tasks", json=task_vide)

    # assert : vérification que la création est refusée avec 422
    assert response.status_code == 422


def test_get_nonexistent_task(client):
    """Demander une tâche qui n'existe pas renvoie 404."""
    # arrange : on prend un ID qui n'existe pas (par exemple 67676767)
    nonexistent_id = 67676767

    # act demande de la tâche inexistante
    response = client.get(f"/tasks/{nonexistent_id}")

    # assert : vérification que la réponse est 404
    assert response.status_code == 404


def test_update_task_with_invalid_priority(client):
    """Mettre à jour une tâche avec priority="urgent" est refusé : 422.
    (Les priorités valides sont "low", "medium" et "high".)"""
    # arrange : préparation de la tâche valide à modifier
    create_response = client.post("/tasks", json={"title": "Tâche valide", "priority": "medium"})
    task_id = create_response.json()["id"]

    # act : tentative de mise à jour avec une priorité invalide
    response = client.put(f"/tasks/{task_id}", json={"priority": "urgent"})

    # assert : 422 = Erreur de Validation
    assert response.status_code == 422
    # tache non modifiée
    assert client.get(f"/tasks/{task_id}").json()["priority"] == "medium"


def test_filter_tasks_by_status(client):
    """Créez une tâche "todo" et une tâche "done" : GET /tasks?status=done
    ne renvoie qu'une seule tâche, celle qui est terminée."""
    # arrange : creation de deux tâches avec des statuts différents : à faire et terminée
    client.post("/tasks", json={"title": "Tâche à faire", "status": "todo"})
    client.post("/tasks", json={"title": "Tâche terminée", "status": "done"})

    # act : filtrage des tâches par statut "done"
    response = client.get("/tasks?status=done")

    #assert : vérification qu'une seule tâche est renvoyée et que c'est bien celle terminée
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Tâche terminée"
    assert tasks[0]["status"] == "done"


# =============================================================================
# BONUS (si vous avez fini)
# =============================================================================
#
# Supprimez la ligne @pytest.mark.skip(...) pour activer un test.

@pytest.mark.skip(reason="Bonus : supprimez cette ligne pour écrire le test")
def test_filter_by_status_and_priority(client):
    """GET /tasks?status=todo&priority=high combine les deux filtres."""
    pytest.fail("Test à écrire (Bonus)")


@pytest.mark.skip(reason="Bonus : supprimez cette ligne pour écrire le test")
def test_create_task_with_title_too_long(client):
    """Le titre est limité à 200 caractères : 200 est accepté (201), 201 est refusé (422).
    Astuce : "a" * 200 crée un texte de 200 caractères."""
    pytest.fail("Test à écrire (Bonus)")


# =============================================================================
# ASTUCES & CONSEILS
# =============================================================================

"""
PATTERNS COURANTS :

1. Tester POST (Créer) :
   response = client.post("/tasks", json={"title": "..."})
   assert response.status_code == 201

2. Tester GET (Lire) :
   response = client.get("/tasks")
   assert response.status_code == 200

3. Tester PUT (Mettre à jour) :
   response = client.put(f"/tasks/{id}", json={"title": "..."})
   assert response.status_code == 200

4. Tester DELETE (Supprimer) :
   response = client.delete(f"/tasks/{id}")
   assert response.status_code == 204

5. Tester les erreurs de validation :
   response = client.post("/tasks", json={"bad": "data"})
   assert response.status_code == 422

6. Tester les erreurs 404 (la ressource demandée n'existe pas) :
   assert response.status_code == 404

CODES DE STATUT COURANTS :
- 200 : OK (GET/PUT réussi)
- 201 : Créé (POST réussi)
- 204 : Pas de Contenu (DELETE réussi)
- 404 : Non Trouvé (la ressource n'existe pas)
- 422 : Erreur de Validation (données invalides)

RAPPELEZ-VOUS :
- La fixture `client` est automatiquement fournie par conftest.py
- Les tâches sont automatiquement effacées avant/après chaque test (fixture clean_tasks)
- Les tests doivent être indépendants (ne pas dépendre d'autres tests)
"""
