import firebase_admin
from firebase_admin import credentials, auth
from flask import Flask, json, request, jsonify
import time
import google.auth.crypt
import google.auth.jwt
import os

app = Flask(__name__)

cred = credentials.Certificate('cred.json')
firebase_admin.initialize_app(cred)


# Authenticates the token passed and checks email verification
def authenticate(token):
    try:
        return auth.verify_id_token(token)['email_verified']
    except:
        return False


def generate_jwt(sa_keyfile='cred.json',
                 sa_email='firebase-adminsdk-gwxlx@uw-ideas-ai-psychophysiology.iam.gserviceaccount.com',
                 audience='uw-ideas-ai-psychophysiology',
                 expiry_length=3600):
    """Generates a signed JSON Web Token using a Google API Service Account."""

    now = int(time.time())

    # build payload
    payload = {
        'iat': now,
        "exp": now + expiry_length,
        'iss': sa_email,
        'aud': audience,
        'sub': sa_email,
        'email': sa_email
    }

    # sign with keyfile
    signer = google.auth.crypt.RSASigner.from_service_account_file(sa_keyfile)
    jwt = google.auth.jwt.encode(signer, payload)
    return jwt


@app.route('/get_access_token', methods=['GET'])
def get_access_token():
    token = request.args.get("token")
    try:
        if authenticate(token):
            return generate_jwt()
        else:
            return 'unauthorized', 401
    except:
        return 'error', 500


# Starting application on 8080 port
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
