"""Tests for api server"""
import requests
import io
from app import app


def test_index_redirect():
    """Checks getting index redirects to main site"""
    tester = app.test_client()
    response = tester.get("/")
    assert response.status_code == 302


def test_encrypt_resume_misc():
    """Tests misc features of the encrypt resume EP"""
    tester = app.test_client()
    redirect = tester.get("/encrypted_resume")
    assert redirect.status_code == 302
    no_key = tester.post("/encrypted_resume")
    assert no_key.status_code == 400


def test_encrypt_resume():
    """Tests main section of the encrypt resume EP"""
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
