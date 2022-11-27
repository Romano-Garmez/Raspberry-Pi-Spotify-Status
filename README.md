# Harvard CS50 Final Project: Spotify Status
#### Video Demo: https://youtu.be/Yc1qeze1bso

#### Description:
A web app to display your currently playing song on Spotify. Allows you to skip songs, play/pause, and like/unlike. Analyzes album artwork to choose background and foreground color to match the image. Polls every two seconds to refresh the display to show your currently playing song. Scales to the size of your display using dynamic layout.

#### Screenshots:

![Always This Late](https://i.imgur.com/iub38zU.jpg)

![Swim](https://i.imgur.com/HElS7Fv.jpg)

![R U Mine?](https://i.imgur.com/p05nO9v.jpg)

#### Implementation:
I started my project by setting up a basic site to show raw JSON of my Spotify data utilizing [Spotipy](https://github.com/plamere/spotipy), an open source Spotify Python API. Later on, I wrote some javascript to poll the Spotify API every two seconds to check for changes. If the song has changed, the page is refreshed with the new info.

I compute the color palette using a javascript library called [ColorThief](https://github.com/lokesh/color-thief) which grabs the dominant color for the background, and a contrasting alternate color from the palette for the text. The text color is not just black or white, but instead samples a few alternate colors to form an entire palette, and finds a color from that palette that contrasts with the selected background color.

I use [Google Material Symbols](https://material.io/blog/introducing-symbols) for the playback control icons. This allows for easy scaling to different screen sizes without needing separate images.

#### Difficulties and Struggles:
Getting arrangement of elements on screen and scaling for different displays was a challenge. I wanted it to look at least tolerable on anything from a PC with a landscape screen, to something like a mobile phone. It isn't perfect, but it's fairly solid. Additionally, finding at what point the text should be white instead of black was difficult. I had to make sure that the song details would be easily readable no matter what song was playing at that moment.

#### Future Plans:
I intend to use this projects on a Raspberry Pi with a screen in my dining room. For this to work, I need a couple extra things sorted out. I want the project to be able to turn off the screen when no songs are playing, rather than display a blank screen. For this, I already have a Java webserver running on my Raspberry Pi from a previous project, so that should be easy. Additionally, I plan to apply for a quota extension request on the Spotify developer site so more people can use this without having to host it themselves. 

I will keep this CS50 version as a separate branch before I make any of these additional changes.

#### Files:
* app.py: Python code for Flask server. Uses Spotipy API for the backend, logs you in, polls Spotify API
* static/styles.css: Visual customizations, uses Bootstrap
* templates/currently_playing.html: Main web page, shows album art, song details and playback controls
* templates/layout.html: Template page, imports Bootstrap, runs polling code
* templates/login.html: Sign-in page
* templates/not_playing.html: Displayed if no song currently playing

