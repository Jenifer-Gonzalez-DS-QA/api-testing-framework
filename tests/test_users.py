import pytest
from utils.api_client import APIClient

# ── JSONPlaceholder /users ────────────────────────────────────────────────────
# GET /users       → lista de 10 usuarios
# GET /users/1     → {“id”:1,“name”:”…”,“username”:”…”,“email”:”…”,“address”:{…}}
# GET /users/9999  → 404
# POST /users      → 201
# PUT /users/1     → 200
# PATCH /users/1   → 200
# DELETE /users/1  → 200

BASE_URL = "https://jsonplaceholder.typicode.com"
client = APIClient(BASE_URL)


class TestGetUsers:
    """Pruebas GET para el recurso /users"""

    def test_get_users_status_200(self):
        """Lista de usuarios devuelve 200"""
        response = client.get("/users")
        assert response.status_code == 200

    def test_get_users_is_list(self):
        """La respuesta es una lista"""
        response = client.get("/users")
        assert isinstance(response.json(), list)

    def test_get_users_total_10(self):
        """JSONPlaceholder tiene exactamente 10 usuarios"""
        response = client.get("/users")
        assert len(response.json()) == 10

    def test_get_single_user_status_200(self):
        """Obtener usuario por ID devuelve 200"""
        response = client.get("/users/1")
        assert response.status_code == 200

    def test_get_single_user_fields(self):
        """El usuario tiene los campos esperados"""
        response = client.get("/users/1")
        user = response.json()
        assert "id" in user
        assert "name" in user
        assert "username" in user
        assert "email" in user

    def test_get_single_user_correct_id(self):
        """El ID devuelto coincide con el solicitado"""
        response = client.get("/users/1")
        assert response.json()["id"] == 1

    def test_get_user_not_found_404(self):
        """Usuario inexistente devuelve 404"""
        response = client.get("/users/9999")
        assert response.status_code == 404

    def test_get_user_posts(self):
        """Obtener posts de un usuario específico"""
        response = client.get("/users/1/posts")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestCreateUser:
    """Pruebas POST para crear usuarios"""

    def test_create_user_status_201(self):
        """Crear usuario devuelve 201"""
        payload = {"name": "Jenifer QA",
                   "username": "jeniferqa", "email": "jenifer@qa.com"}
        response = client.post("/users", json=payload)
        assert response.status_code == 201

    def test_create_user_returns_id(self):
        """El usuario creado tiene un ID"""
        payload = {"name": "Jenifer QA",
                   "username": "jeniferqa", "email": "jenifer@qa.com"}
        response = client.post("/users", json=payload)
        data = response.json()
        assert "id" in data

    def test_create_user_data_matches(self):
        """Los datos enviados se reflejan en la respuesta"""
        payload = {"name": "Jenifer QA",
                   "username": "jeniferqa", "email": "jenifer@qa.com"}
        response = client.post("/users", json=payload)
        data = response.json()
        assert data["name"] == "Jenifer QA"
        assert data["email"] == "jenifer@qa.com"


class TestUpdateUser:
    """Pruebas PUT y PATCH para actualizar usuarios"""

    def test_update_user_put_status_200(self):
        """PUT devuelve 200"""
        payload = {"id": 1, "name": "Jenifer Updated",
                   "username": "jeniferqa", "email": "j@qa.com"}
        response = client.put("/users/1", json=payload)
        assert response.status_code == 200

    def test_update_user_patch_status_200(self):
        """PATCH devuelve 200"""
        payload = {"email": "jenifer.new@qa.com"}
        response = client.patch("/users/1", json=payload)
        assert response.status_code == 200

    def test_update_user_patch_data_matches(self):
        """PATCH devuelve el campo actualizado"""
        payload = {"name": "Jenifer Patch"}
        response = client.patch("/users/1", json=payload)
        assert response.json()["name"] == "Jenifer Patch"


class TestDeleteUser:
    """Pruebas DELETE para usuarios"""

    def test_delete_user_status_200(self):
        """DELETE devuelve 200"""
        response = client.delete("/users/1")
        assert response.status_code == 200

    def test_delete_user_empty_response(self):
        """DELETE devuelve objeto vacío"""
        response = client.delete("/users/1")
        assert response.json() == {}
