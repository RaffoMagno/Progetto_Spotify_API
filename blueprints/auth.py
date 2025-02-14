from flask import Blueprint, redirect, request, url_for, session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "b1ed2d5909a24d66912adc6f42531fee"
SPOTIFY_CLIENT_SECRET = "db711b1f9ba646b1a5d1c4cbe0cf897b"
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettospot-yp2lqjzcg6l.ws-eu117.gitpod.io/callback"

auth_bp = Blueprint('auth', __name__)

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private",
    show_dialog=True
)

@auth_bp.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/logout')
def logout():
    session.clear()  # Cancella l'access token salvato in sessione
    return redirect(url_for('auth.login'))

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('home.homepage'))