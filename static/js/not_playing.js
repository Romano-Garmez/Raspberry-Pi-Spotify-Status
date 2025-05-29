var turnOffRequest = new XMLHttpRequest();
turnOffRequest.open("GET", "http://localhost:9000/TurnOffScreen", true); // false for synchronous request
turnOffRequest.send(null);

function reqListener() {
    var parsed = JSON.parse(this.responseText)
    //console.log(parsed)

    if (!parsed["same_track"]) {
        location.reload();
    }
}
function reloadPageListener() {
    location.reload();
}

function compareTrack() {
    try {
        const req = new XMLHttpRequest();
        req.addEventListener("load", reqListener);
        req.addEventListener("error", reloadPageListener)
        req.open("GET", "/current_track_xhr?id={{id}}&currently_playing={{currently_playing}}");
        req.send();
    } catch (error) {
        console.log("Unable to reach server");
        location.reload();
    }
}

const interval = setInterval(function () {
    compareTrack()
}, 2000);