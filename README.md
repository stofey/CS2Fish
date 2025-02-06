# CS2Fish

Ingame chat self bot to fish and gamble


### Features
- !fish to fish (duh)
- !balance to see a users balance and biggest fish caught
- !gamble [int] or all to gamble with the balance

### Dependencies
`pip install pydirectinput`

### Setup

- download pyth form https://www.python.org/downloads/ (make sure to check "Add to Path" during installation)
- open shell/cmd
- type `pip install pydirectinput`
- download the CS2Fish Folder
- create a message.cfg file in `SteamLibrary\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg`
- add `bind l "exec message"` to your autoexec (this can be changed by replacing the key in the fish.py file where the comments are)
- replace the path to your csgo\cfg folder in the main.py file
- put `-condebug -conclearlog` in your CS2 launch option
