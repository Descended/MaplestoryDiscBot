# MaplestoryDiscBot


## Overview
  MaplestoryDiscBot is a Python-based Discord Bot designed for MapleStory private servers.
  
  This bot allows direct access to and/or manipulation of data via the database, as well as through web-requests (proprietary API).

## SETUP
### For the setup guide see the guide on the [wiki](https://github.com/Descended/MaplestoryDiscBot/wiki/Setup)

## Features
### General Commands
  - Display help page
    - `!help` or `!commands`
  - Display character info
    - `!character` or `!char` or `!player`
  - Display guild info
    - `!guild` or `!guildinfo`
  - Display ranking
    - `!rankings` or `!ranking` or `!ranktop`
  - Display online players
    - `!online`
  - Display credits
    - `!credits` or `!credit`
  
### Admin Commands  
  - Transfer items
    - `!duey` or `!giveitem`
  - Disconnect player
    - `!dc`
  - Whisper to player in-game
    - `!whisper` or `!msg`
  - Post in-game notice
    - `!notice`
  - Unban player in-game
    - `!unban` or `!pardon`
  - Promote player to GM in-game
    - `!setgmlevel` or `!makegm`

## Gallery
*Images pending. To be appended when RC1 is ready.*
## Miscellaneous
### Technical Details
##### Current Version: v0.0.15 Alpha  
Changelog: [changelog.md](changelog.md)

|  | Targeted | Tested |
|---|---|---|
| Python | 3.6 | ? |  

### Auto-launch:
Run the batch file `start.bat`

---
### Manual launch:
#### Option A: Using the virtual environment
The virtual environment is part of the repository (as of time of writing).  
You may use it after cloning without needing to set it up yourself.
##### Command Prompt route:
  - Activate the virtual environment using `call venv\scripts\activate.bat`
    - Note: You can deactivate the venv by using the command deactivate
  - Use the command `venv\scripts\python src/Main.py` to run
##### PowerShell route: 
  - Activate the virtual environment using `venv\scripts\activate`
    - Note: You can deactivate the venv by using the command deactivate
  - Use the command `venv\scripts\python src/Main.py` to run  
    
  
#### Option B: Using the global environment
  - `python src/Main.py`

---

### Notes prior to use
Please read the license agreement prior to use, since the act of using this software implies agreement to the license. Note in particular the opening statement, as well as Section 13 of the AGPL license.
