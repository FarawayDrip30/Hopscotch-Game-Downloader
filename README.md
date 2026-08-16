# Hopscotch Game Downloader
## v0.1.0
A Python script that automatically downloads Hopscotch games and the files needed to run them, even offline, so people can archive their Hopscotch games.

NOTE: So far, games can be downloaded and functionally ran offline, but there are still a few issues to solve:
* Avenir_Roman.woff2 not loaded correctly in style.css.
* speaker.svg's path is incorrect for some reason.
* Loading gifs are not downloaded.
* When offline, the browser's default emojis are used instead of the usual iOS ones.

At some point I may also pack a python http server library into "hopscotch_game_downloader.py" so you do not need to download any other programs to run your games, and maybe compile it to an .exe with pyinstaller for ease of use.

## How To Use
### Setup
1. Clone or download this repo.
2. Make sure Python is installed, and install it if not.
3. Install pycurl with "pip install pycurl" or "pip install -r requirements.txt".

### Downloading HopscotchData
The HopscotchData folder contains all of the files that game .html files need to run. 
1. Run the "hopscotch_game_downloader.py" file.
2. Input "2" for "Download HopscotchData" and press enter in the program console that opens up, and wait for HopscotchData to finish downloading. It will download to the same directory that "hopscotch_game_downloader.py" is in.

### Downloading a Game
1. Go to the webpage of the game that you want to download. The URL in your browser should look something like "https://www.gethopscotch.com/2622605/12v2mgu1zn", or "https://explore.gethopscotch.com/e/xcdpx21ev" or something. If it looks a bit different, don't worry, you just need to copy the short code after the last "/" from it.
2. Run the "hopscotch_game_downloader.py" file.
3. Press "1" for "Download Game".
4. Paste in the code that you copied from the URL.
5. Enter the name of your game.
6. Wait for the game to download. It will download to the same directory that "hopscotch_game_downloader.py" is in, as a ".html" file.

### Running a Game
Eventually I will add a http-server module in python so you don't need to use node.js, but for now, here's how you do it:
(note you can use any other way of hosting a local / not local webserver to do this)
1. Download Node.js.
2. Run "npm install http-server -g" in your Command Terminal.
3. Ensure the .html file of the game you want to play is in the same directory as your HopscotchData folder.
4. With your Command Terminal in the same directory as your game and HopscotchData folder, run "http-server" in your terminal.
5. Copy and paste the provided links from the terminal into your browser (e.g. "http://192.168.0.100:8081" or  "http://127.0.0.1:8081")
6. Click on the gamename.html link for the game you want to play (Note: If your game is not there, try pressing CTRL+SHIFT+R to refresh the page and reset your cache)
7. Hey Presto! You are now playing your awesome hopscotch game.