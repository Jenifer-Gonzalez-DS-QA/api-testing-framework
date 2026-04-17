import pytest
from utils.api_client import APIClient

# ── JSONPlaceholder /comments y /todos ───────────────────────────────────────
# GET /comments           → lista de 500 comentarios
# GET /comments/1         → comentario por ID
# GET /comments?postId=1  → comentarios de un post
# GET /todos/1            → {“userId”:1,“id”:1,“title”:”…”,“completed”:false}
# GET /todos?completed=true → todos completados

BASE_URL = "https://jsonplaceholder.typicode.com"
client = APIClient(BASE_URL)


class TestComments:
    """Pruebas para el recurso /comments"""

    def test_get_comments_status_200(self):
        """Lista de comentarios devuelve 200"""
        response = client.get("/comments")
        assert response.status_code == 200

    def test_get_comments_is_list(self):
        """La respuesta es una lista"""
        response = client.get("/comments")
        assert isinstance(response.json(), list)

    def test_get_comment_by_id_status_200(self):
        """Obtener comentario por ID devuelve 200"""
        response = client.get("/comments/1")
        assert response.status_code == 200

    def test_get_comment_fields(self):
        """El comentario tiene los campos esperados"""
        response = client.get("/comments/1")
        comment = response.json()
        assert "postId" in comment, "Falta 'postId'"
        assert "id" in comment, "Falta 'id'"
        assert "name" in comment, "Falta 'name'"
        assert "email" in comment, "Falta 'email'"
        assert "body" in comment, "Falta 'body'"

    def test_get_comment_email_format(self):
        """El email del comentario contiene @"""
        response = client.get("/comments/1")
        email = response.json()["email"]
        assert "@" in email, f"El email '{email}' no tiene formato válido"

    def test_filter_comments_by_post(self):
        """Filtrar comentarios por postId devuelve solo los de ese post"""
        response = client.get("/comments", params={"postId": 1})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for comment in data:
            assert comment["postId"] == 1

    def test_get_comment_not_found_404(self):
        """Comentario inexistente devuelve 404"""
        response = client.get("/comments/9999")
        assert response.status_code == 404

    def test_create_comment_status_201(self):
        """Crear comentario devuelve 201"""
        payload = {
            "postId": 1,
            "name":  "QA Test Comment",
            "email": "jenifer@qa.com",
            "body":  "Comentario de prueba automatizado"
        }
        response = client.post("/comments", json=payload)
        assert response.status_code == 201

    def test_create_comment_data_matches(self):
        """Los datos del comentario creado coinciden"""
        payload = {
            "postId": 1,
            "name":  "QA Test",
            "email": "jenifer@qa.com",
            "body":  "Body QA"
        }
        response = client.post("/comments", json=payload)
        data = response.json()
        assert data["email"] == "jenifer@qa.com"
        assert data["name"] == "QA Test"


class TestTodos:
    """Pruebas para el recurso /todos"""

    def test_get_todos_status_200(self):
        """Lista de todos devuelve 200"""
        response = client.get("/todos")
        assert response.status_code == 200

    def test_get_todo_by_id_status_200(self):
        """Todo por ID devuelve 200"""
        response = client.get("/todos/1")
        assert response.status_code == 200

    def test_get_todo_fields(self):
        """El todo tiene los campos esperados"""
        response = client.get("/todos/1")
        todo = response.json()
        assert "userId" in todo, "Falta 'userId'"
        assert "id" in todo, "Falta 'id'"
        assert "title" in todo, "Falta 'title'"
        assert "completed" in todo, "Falta 'completed'"

    def test_get_todo_completed_is_bool(self):
        """El campo 'completed' es booleano"""
        response = client.get("/todos/1")
        todo = response.json()
        assert isinstance(todo["completed"], bool)

    def test_get_todo_not_found_404(self):
        """Todo inexistente devuelve 404"""
        response = client.get("/todos/9999")
        assert response.status_code == 404

    def test_filter_todos_by_user(self):
        """Filtrar todos por userId funciona"""
        response = client.get("/todos", params={"userId": 1})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0
        for todo in data:
            assert todo["userId"] == 1
