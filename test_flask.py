"""Tests for api server."""
import io
import requests
from app import app


def test_index_redirect():
    """Checks getting index redirects to main site."""
    tester = app.test_client()
    response = tester.get("/")
    assert response.status_code == 302


def test_encrypt_resume_misc():
    """Tests misc features of the encrypt resume EP."""
    tester = app.test_client()
    redirect = tester.get("/encrypted_resume")
    assert redirect.status_code == 302
    no_key = tester.post("/encrypted_resume")
    assert no_key.status_code == 400


def test_encrypt_resume():
    """Tests main section of the encrypt resume EP."""
    tester = app.test_client()
    download = requests.get(
            "https://portfolio.jwhite.network/keys/WebsitePublic.asc"
        )
    data = dict(key=(io.BytesIO(download.content), "key.asc"))

    response = tester.post(
        "/encrypted_resume",
        data=data,
        buffered=True,
        headers={"Content-Type": "multipart/form-data"}
        )

    assert response.status_code == 200


def test_git_user():
    """Tests git user endpoint"""
    tester = app.test_client()
    response = tester.get(
        "/git/user"
    )
    assert response.status_code == 200
    assert len(response.json) == 30


def test_repo():
    """Tests git repo endpoint"""
    tester = app.test_client()
    response = tester.get(
        "/git/repos"
    )
    assert response.status_code == 200
    assert len(response.json) == 30


def test_repo_list():
    """Tests git repo endpoint"""
    tester = app.test_client()
    response = tester.get(
        "/git/repos/list"
    )
    assert response.status_code == 200
    assert len(response.json) == 30


def test_404():
    """Tests 404 handling"""
    tester = app.test_client()
    response = tester.get(
        "/404"
    )
    assert response.status_code == 404
    assert response.json["Error"] == "Route does not exist"
