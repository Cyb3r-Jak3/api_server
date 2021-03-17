"""Main Web runner thing."""
import io
import os
import tempfile
from flask import Flask, request, redirect, send_file, jsonify
from flask_cors import CORS
import gnupg
import requests

app = Flask(__name__)
CORS(app, origins=["jwhite.network"], methods=["GET", "OPTIONS", "POST"])

tmpdir = tempfile.mkdtemp()
gpg = gnupg.GPG(gnupghome=tmpdir)


def get_resume():
    """Downloads resumse from my website"""
    if not os.path.exists("resume.pdf"):
        req = requests.get(
            "https://www.jwhite.network/resumes/JacobWhiteResume.pdf"
        )
        with open("resume.pdf", mode="wb") as new_resume:
            new_resume.write(req.content)


def encrypt_resume(file):
    """Encrypts my resumse with the given key."""
    imported_key = gpg.import_keys(file.read()).fingerprints[0]
    with open("resume.pdf", mode="rb") as resumse:
        encrypted_data = gpg.encrypt_file(
            resumse, imported_key, always_trust=True
        )
    gpg.delete_keys(imported_key)
    return encrypted_data.data


@app.route("/")
def home():
    """Redirects anyone to my website."""
    return redirect("https://www.jwhite.network")


@app.route("/encrypted_resume", methods=["GET", "POST"])
def encrypt_resume_ep():
    """Encrypts my resume with any public key sent."""
    if request.method == "GET":
        return redirect("https://www.jwhite.network")
    try:
        new_key = request.files["key"]
    except KeyError:
        return "There was no file in the request", 400
    return send_file(
        io.BytesIO(encrypt_resume(new_key)),
        attachment_filename="jwhite_signed_resume.pdf.gpg",
        as_attachment=True,
    )


@app.route("/git/user", methods=["GET"])
def git_user():
    """Get My GitHub Info"""
    hub_req = requests.get(
        "https://api.github.com/users/Cyb3r-Jak3",
        headers={"Accept": "application/vnd.github.v3+json"},
    ).json()
    hub_req["email"] = "cyb3rjak3@pm.me"
    hub_req["github_url"] = hub_req["html_url"]
    _ = [
        hub_req.pop(item, None)
        for item in ["public_gists", "html_url", "gists_url", "company"]
    ]
    lab_req = requests.get(
        "https://gitlab.com/api/v4/users?username=cyb3r-jak3"
    ).json()[0]
    hub_req["gitlab_url"] = lab_req["web_url"]
    return jsonify(hub_req)


@app.route("/git/repos", methods=["GET"])
def git_repos():
    """Get My Github Repos"""
    req = requests.get(
        "https://api.github.com/users/Cyb3r-Jak3/repos",
        headers={"Accept": "application/vnd.github.v3+json"},
    ).json()
    return jsonify(req)


@app.route("/git/repos/list", methods=["GET"])
def git_repos_list():
    """Get My Github Repos as a list"""
    req = requests.get(
        "https://api.github.com/users/Cyb3r-Jak3/repos",
        headers={"Accept": "application/vnd.github.v3+json"},
    ).json()
    list_of_repos = [{repo["name"]: repo["html_url"]} for repo in req]
    return jsonify(list_of_repos)


@app.errorhandler(404)
def handle_404(_):
    """Handle 404 Errors"""
    return jsonify({"Error": "Route does not exist"}), 404


if __name__ == "__main__":  # pragma: no cover
    get_resume()
    app.run(port=5001)
