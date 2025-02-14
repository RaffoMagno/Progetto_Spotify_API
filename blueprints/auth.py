from flask import Blueprint, redirect, request, url_for, session
from services.spotify_oauth import sp_oauth, get_spotify_object

auth_bp = Blueprint('auth', __name__) #creiamo il blueprint

@auth_bp.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@auth_bp.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code) #otteniamo il token
    session['token_info'] = token_info #lo salviamo in session
    return redirect(url_for('home.home')) #richiamiamo il metodo home nel blueprint playlist

@auth_bp.route('/logout')
def logout():
    session.clear() #cancelliamo la sessione
    return redirect(url_for('auth.login')) #metodo login nel blueprint auth