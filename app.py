from flask import Flask, redirect, request, url_for, render_template,session
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_CLIENT_ID = "b1ed2d5909a24d66912adc6f42531fee"
SPOTIFY_CLIENT_SECRET = "db711b1f9ba646b1a5d1c4cbe0cf897b"
SPOTIFY_REDIRECT_URI = "https://5000-raffomagno-progettospot-yp2lqjzcg6l.ws-eu117.gitpod.io/callback"

app = Flask(__name__)
app.secret_key = 'chiave_per_session'

sp_oauth = SpotifyOAuth(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    redirect_uri=SPOTIFY_REDIRECT_URI,
    scope="user-read-private",
    show_dialog=True
)

@app.route('/')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/logout')
def logout():
    session.clear() #cancelliamo l'access token salvato in session
    return redirect(url_for('login'))

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('home'))

@app.route('/visualizza_brani/<playlist_id>')
def visualizza_brani(playlist_id):
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    tracks_data = sp.playlist_tracks(playlist_id)  # Ottieni i brani della playlist
    tracks = tracks_data['items']

    return render_template('brani.html', tracks=tracks)


@app.route('/home')
def home():
    token_info = session.get('token_info', None) #recupero token sissione (salvato prima)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token']) #usiamo il token per ottenere i dati del profilo
    user_info = sp.current_user()
    print(user_info) #capiamo la struttura di user_info per usarle nel frontend
    playlists = sp.current_user_playlists()
    playlists_info = playlists['items']
    return render_template('home.html', user_info=user_info, playlists=playlists_info)

if __name__ == '__main__':
    app.run(debug=True)