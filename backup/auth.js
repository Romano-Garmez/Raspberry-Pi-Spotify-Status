client_id = "---";
redirect_uri = 'http://192.168.86.20:5000/login-success';
scopes = "user-read-currently-playing";

function login() {
  location.href=`https://accounts.spotify.com/authorize?client_id=${this.client_id}&response_type=token&redirect_uri=${this.redirect_uri}&scope=${this.scopes}&show_dialog=true`
}
