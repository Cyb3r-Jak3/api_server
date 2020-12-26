"""Main Web runner thing."""
import io
import os
import tempfile
from flask import Flask, request, redirect, send_file
from flask_cors import CORS
import gnupg
import requests


tmpdir = tempfile.mkdtemp()
gpg = gnupg.GPG(gnupghome=tmpdir)

if not os.path.exists("resume.pdf"):
    r = requests.get("https://www.jwhite.network/resumes/JacobWhiteResume.pdf")
    with open("resume.pdf", mode="wb") as new_resume:
        new_resume.write(r.content)

app = Flask(__name__)
CORS(app, origins=["jwhite.network"])


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


if __name__ == "__main__":  # pragma: no cover
    app.run(port=5001)
