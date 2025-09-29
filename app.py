from flask import Flask, redirect, request, session, url_for, render_template
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

CLIENT_ID = os.getenv('STRAVA_CLIENT_ID')
CLIENT_SECRET = os.getenv('STRAVA_CLIENT_SECRET')
REDIRECT_URI = os.getenv('STRAVA_REDIRECT_URI')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/authorize')
def authorize():
    return redirect(
        f"https://www.strava.com/oauth/authorize?client_id="
        f"{CLIENT_ID}&response_type=code&redirect_uri="
        f"{REDIRECT_URI}&approval_prompt=force&scope=activity:read"
    )

@app.route('/callback')
def callback():
    code = request.args.get('code') # retrieve auth code from request
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'code': code,
            'grant_type': 'authorization_code'
        }
    )
    data = response.json()
    session['access_token'] = data['access_token']
    return redirect(url_for('activities'))

@app.route('/activities')
def activities():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('home'))

    response = requests.get(
        "https://www.strava.com/api/v3/athlete/activities",
        headers={'Authorization': f'Bearer {access_token}'}
    )
    activities = response.json()
    return {
        'activities': activities[:5],  # Return the first 5 activities for now
    }

if __name__ == '__main__':
    app.run(debug=True)