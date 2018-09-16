
# pytest automatically injects fixtures
# that are defined in conftest.py
# in this case, client is injected
def test_index(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["result"]["content"] == "hello world!"


def test_mirror(client):
    res = client.get("/mirror/Tim")
    assert res.status_code == 200
    assert res.json["result"]["name"] == "Tim"


def test_get_users(client):
    res = client.get("/users")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 4
    assert res_users[0]["name"] == "Aria"


def tests_get_users_with_team(client):
    res = client.get("/users?team=LWB")
    assert res.status_code == 200

    res_users = res.json["result"]["users"]
    assert len(res_users) == 2
    assert res_users[1]["name"] == "Tim"


def test_get_user_id(client):
    res = client.get("/users/1")
    assert res.status_code == 200

    res_user = res.json["result"]["user"]
    assert res_user["name"] == "Aria"
    assert res_user["age"] == 19


def test_post_user(client):
    res = client.post("/users", json={"name": "helena", "age": 19, "team": "C2TC"})
    assert res.status_code == 201
    res_user = res.json
    assert res_user["name"] == "helena"
    assert res_user["age"] == 19
    assert res_user["team"] == "C2TC"
    assert res_user["id"] is not None


def test_put_user(client):
    res = client.put("/users/1", json={"age": 20, "team": "LWB"})
    assert res.status_code == 201
    res_user = res.json
    assert res_user["name"] == "Aria"  # Unchanged Value
    assert res_user["age"] == 20  # changed
    assert res_user["team"] == "LWB"  # changed


def test_delete_user(client):
    res = client.delete("/users/1")
    assert res.status_code == 200
    res_user = res.json
    assert res_user["message"] == "Deletion of Data Successful"  # Unchanged Value


## TESTING FOR BAD INPUTS


def test_bad_post_user(client):
    res = client.post("/users", json={"name": "helena", "team": "C2TC"})
    assert res.status_code == 422


def test_get_bad_user_id(client):
    res = client.get("/users/9")
    assert res.status_code == 404


def test_get_bad_delete_user(client):
    res = client.delete("/users/9")
    assert res.status_code == 404
