import pytest, os, sys, tempfile, mock, json
from flask import Flask


@pytest.fixture
def client():
    with mock.patch('flask.Flask', lambda x: Flask(x)):
        from app import app
        db_fd, app.config['DATABASE'] = tempfile.mkstemp()
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
        os.close(db_fd)
        os.unlink(app.config['DATABASE'])


@pytest.mark.it("La estructura Family debe inicializarse con los 3 miembros especificados en las instrucciones")
def test_first_three(client):
    response = client.get('/members')
    members = json.loads(response.data)
    assert len(members) == 3, "La estructura Family debe inicializarse con los 3 miembros especificados en las instrucciones"


@pytest.mark.it("Implementa el método POST /members para agregar un nuevo miembro")
def test_add_implementation(client):
    response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [34, 65, 23, 4, 6]
    })
    assert response.status_code == 200, "Implementa el método POST /members para agregar un nuevo miembro"


@pytest.mark.it("El método POST /members debe devolver algo, NO VACÍO")
def test_add_empty_response_body(client):
    response = client.post('/members', json={
        "first_name": "Sandra",
        "age": 12,
        "lucky_numbers": [12, 34, 33, 45, 32, 12]
    })
    assert response.data != b"", "El método POST /members debe devolver algo, NO VACÍO"


@pytest.mark.it("Implementa el método GET /members")
def test_get_members_exist(client):
    response = client.get('/members')
    assert response.status_code == 200


@pytest.mark.it("El método GET /members debe devolver una lista")
def test_get_members_returns_list(client):
    response = client.get('/members')
    data = json.loads(response.data)
    assert isinstance(data, list), "El método GET /members debe devolver una lista"


@pytest.mark.it("Agregamos dos miembros usando POST /members, por lo tanto al llamar a GET /members debe devolver una lista de longitud == 5")
def test_get_members_returns_list_of_five(client):
    response = client.get('/members')
    members = json.loads(response.data)
    assert len(members) == 5, "Agregamos dos miembros usando POST /members, por lo tanto al llamar a GET /members debe devolver una lista de longitud == 5"


@pytest.mark.it("El método GET /members/<int:id> debe existir")
def test_get_single_member_implemented(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1, 2, 3]
    })
    tommy = json.loads(post_response.data)
    get_response = client.get(f"/members/{tommy['id']}")
    assert get_response.status_code == 200, "El método GET /members/<int:id> debe existir"


@pytest.mark.it("El método GET /members/<int:id> debe devolver un único miembro de la familia en formato diccionario")
def test_get_single_member_returns_dict(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1, 2, 3]
    })
    tommy = json.loads(post_response.data)
    get_response = client.get(f"/members/{tommy['id']}")
    data = json.loads(get_response.data)
    assert data is not None, "El método GET /members/<int:id> debe devolver un único miembro de la familia en formato diccionario"
    assert isinstance(data, dict), "El método GET /members/<int:id> debe devolver un único miembro de la familia en formato diccionario"


@pytest.mark.it("El diccionario devuelto por GET /members/<int:id> debe contener las claves: [first_name, id, age, lucky_numbers]")
def test_get_single_member_has_keys(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1, 2, 3]
    })
    tommy = json.loads(post_response.data)
    response = client.get(f"/members/{tommy['id']}")
    data = json.loads(response.data)

    assert data is not None, "El diccionario devuelto por GET /members/<int:id> debe contener las claves: [first_name, id, age, lucky_numbers]"
    assert "first_name" in data, "El diccionario devuelto por GET /members/<int:id> debe contener las claves: [first_name, id, age, lucky_numbers]"
    assert "id" in data, "El diccionario devuelto por GET /members/<int:id> debe contener las claves: [first_name, id, age, lucky_numbers]"
    assert "age" in data
    assert "lucky_numbers" in data


@pytest.mark.it("El método GET /members/<id> debe devolver a Tommy")
def test_get_first_member_tommy(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1]
    })
    tommy = json.loads(post_response.data)
    response = client.get(f"/members/{tommy['id']}")
    data = json.loads(response.data)
    assert data["first_name"] == "Tommy", "El método GET /members/<id> debe devolver a Tommy"


@pytest.mark.it("Implementa el método DELETE /members/<int:id> para eliminar un miembro de la familia")
def test_delete_member(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1, 2, 3]
    })
    tommy = json.loads(post_response.data)
    delete_response = client.delete(f"/members/{tommy['id']}")
    assert delete_response.status_code == 200, "Implementa el método DELETE /members/<int:id> para eliminar un miembro de la familia"


@pytest.mark.it("El método DELETE /members/<id> debe devolver un diccionario con la clave 'done'")
def test_delete_response(client):
    post_response = client.post('/members', json={
        "first_name": "Tommy",
        "age": 23,
        "lucky_numbers": [1, 2, 3]
    })
    tommy = json.loads(post_response.data)
    delete_response = client.delete(f"/members/{tommy['id']}")
    assert delete_response.json["done"] == True, "El método DELETE /members/<id> debe devolver un diccionario con la clave 'done'"