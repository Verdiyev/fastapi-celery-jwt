import requests


def test_login():
    response = requests.post(
        "http://localhost:5000/api/v1/login",
        json={
            "username": "user4",
            "password": "pass"
        }
    )

    assert response.status_code == 200

def test_create_task():
    response = requests.post(
            "http://localhost:5000/api/v1/task",
            json={
                "address": "194.135.152.165"
            }
        )

    assert response.status_code == 200

def test_signup():
    response = requests.post(
        "http://localhost:5000/api/v1/signup",
        json={
            "username": "user4",
            "password": "pass"
        }
    )
    assert response.status_code == 200 or response.status_code == 409

response = requests.post(
            "http://localhost:5000/api/v1/task",
            json={
                "address": "194.135.152.165"
            }
        )
task_id = response.json()["task_id"]
    
def test_task_status():
    response = requests.get(
            f"http://localhost:5000/api/v1/status/{task_id}",
        )

    assert response.status_code == 200

response = requests.post(
        "http://localhost:5000/api/v1/login",
        json={
            "username": "user2",
            "password": "pass"
        }
    )

access_token=response.json()["access_token"]
header = {'Authorization': 'Bearer ' + access_token}

def test_user():
    response = requests.get("http://localhost:5000/user", headers=header)
    assert response.status_code == 200

test_user()