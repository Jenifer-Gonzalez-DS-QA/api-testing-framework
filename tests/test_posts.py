import pytest
from utils.api_client import APIClient

# ── JSONPlaceholder: https://jsonplaceholder.typicode.com ─────────────────────
# Sin registro. Sin API key. 100% gratuito y funciona 24/7.
#
# Estructura GET /posts/1:
# {“userId”: 1, “id”: 1, “title”: “…”, “body”: “…”}
#
# Estructura GET /posts (lista de 100):
# [{“userId”:1,“id”:1,“title”:”…”,“body”:”…”}, …]
#
# POST /posts  → 201  {“id”: 101, “title”: “…”, “body”: “…”, “userId”: 1}
# PUT /posts/1 → 200  {“id”: 1, “title”: “…”, “body”: “…”, “userId”: 1}
# PATCH /posts/1→ 200 {“id”: 1, “title”: “nuevo titulo”, …}
# DELETE /posts/1→200 {}
# GET /posts/9999→404 {}

BASE_URL = "https://jsonplaceholder.typicode.com"
client = APIClient(BASE_URL)


class TestGetPosts:
    """Pruebas GET para el recurso /posts"""

    def test_get_posts_status_200(self):
        """Lista de posts devuelve 200"""
        response = client.get("/posts")
        assert response.status_code == 200

    def test_get_posts_is_list(self):
        """La respuesta es una lista"""
        response = client.get("/posts")
        data = response.json()
        assert isinstance(data, list), "Se esperaba una lista"

    def test_get_posts_total_100(self):
        """JSONPlaceholder tiene exactamente 100 posts"""
        response = client.get("/posts")
        data = response.json()
        assert len(
            data) == 100, f"Se esperaban 100 posts, se obtuvieron {len(data)}"

    def test_get_post_by_id_status_200(self):
        """Obtener un post por ID devuelve 200"""
        response = client.get("/posts/1")
        assert response.status_code == 200

    def test_get_post_by_id_fields(self):
        """El post tiene los campos esperados"""
        response = client.get("/posts/1")
        post = response.json()
        assert "id" in post, "Falta campo 'id'"
        assert "title" in post, "Falta campo 'title'"
        assert "body" in post, "Falta campo 'body'"
        assert "userId" in post, "Falta campo 'userId'"

    def test_get_post_correct_id(self):
        """El ID del post coincide con el solicitado"""
        response = client.get("/posts/1")
        assert response.json()["id"] == 1

    def test_get_post_not_found_404(self):
        """Post inexistente devuelve 404"""
        response = client.get("/posts/9999")
        assert response.status_code == 404

    def test_filter_posts_by_user(self):
        """Filtrar posts por userId devuelve 200 y resultados del usuario"""
        response = client.get("/posts", params={"userId": 1})
        assert response.status_code == 200
        data = response.json()
        assert len(data) > 0, "No se encontraron posts para userId=1"
        for post in data:
            assert post["userId"] == 1, f"Post con userId incorrecto: {post['userId']}"


class TestCreatePost:
    """Pruebas POST para crear posts"""

    def test_create_post_status_201(self):
        """Crear un post devuelve 201"""
        payload = {"title": "Test QA Post",
                   "body": "Contenido de prueba", "userId": 1}
        response = client.post("/posts", json=payload)
        assert response.status_code == 201

    def test_create_post_returns_id(self):
        """El post creado tiene un ID asignado"""
        payload = {"title": "Test QA Post",
                   "body": "Contenido de prueba", "userId": 1}
        response = client.post("/posts", json=payload)
        data = response.json()
        assert "id" in data, "El post creado no tiene ID"
        assert data["id"] == 101, "JSONPlaceholder siempre devuelve id=101 para posts nuevos"

    def test_create_post_data_matches(self):
        """Los datos enviados se reflejan en la respuesta"""
        payload = {"title": "Mi Post QA",
                   "body": "Body de prueba", "userId": 1}
        response = client.post("/posts", json=payload)
        data = response.json()
        assert data["title"] == "Mi Post QA"
        assert data["body"] == "Body de prueba"
        assert data["userId"] == 1


class TestUpdatePost:
    """Pruebas PUT y PATCH para actualizar posts"""

    def test_update_post_put_status_200(self):
        """PUT devuelve 200"""
        payload = {"id": 1, "title": "Título Actualizado",
                   "body": "Body actualizado", "userId": 1}
        response = client.put("/posts/1", json=payload)
        assert response.status_code == 200

    def test_update_post_put_data_matches(self):
        """PUT devuelve los datos actualizados"""
        payload = {"id": 1, "title": "Título Actualizado PUT",
                   "body": "Body", "userId": 1}
        response = client.put("/posts/1", json=payload)
        data = response.json()
        assert data["title"] == "Título Actualizado PUT"
        assert data["id"] == 1

    def test_update_post_patch_status_200(self):
        """PATCH devuelve 200"""
        payload = {"title": "Solo título cambia"}
        response = client.patch("/posts/1", json=payload)
        assert response.status_code == 200

    def test_update_post_patch_data_matches(self):
        """PATCH actualiza solo el campo enviado"""
        payload = {"title": "Título PATCH"}
        response = client.patch("/posts/1", json=payload)
        data = response.json()
        assert data["title"] == "Título PATCH"
        assert data["id"] == 1


class TestDeletePost:
    """Pruebas DELETE"""

    def test_delete_post_status_200(self):
        """DELETE devuelve 200 (JSONPlaceholder no usa 204)"""
        response = client.delete("/posts/1")
        assert response.status_code == 200

    def test_delete_post_returns_empty(self):
        """DELETE devuelve un objeto vacío"""
        response = client.delete("/posts/1")
        assert response.json() == {}
