client_id = "a5a6689bc6f848a8a4a52d732e0de113";
redirect_uri = 'http://127.0.0.1:5000/login-success';
scopes = "user-read-currently-playing";

function login() {
  location.href=`https://accounts.spotify.com/authorize?client_id=${this.client_id}&response_type=token&redirect_uri=${this.redirect_uri}&scope=${this.scopes}&show_dialog=true`
}
