====================
 DAWNFALL OF ELDARA
====================

Description:
-------------------
Dawnfall of Eldara is a simple dungeon crawler inspired by classic turn-based RPGs like Final Fantasy or Might and Magic. Four players form a party of heroes who explore the dungeons of Eldara together. Players take turns performing actions to defeat enemies and uncover hidden treasure—while avoiding their own demise.

This project was created as part of a Client-Server Application Programming course.

Requirements:
-------------------
- Python 3.9 or newer
- Pygame 2.0 or newer

Structure:
-------------------
- server.py     – launches the game server
- client.py     – launches the game client
- game/         – game logic
- ui/           – game screens and GUI-related functions
- assets/       – graphics, fonts, backgrounds

How to Run:
-------------------
1. In the first terminal:
    python server.py

2. In four additional terminals:
    python client.py

Players connect to the server until a full party of 4 is formed — the game starts automatically.
Unlimited amount of rooms can be active, as long as party of 4 is formed.

Controls:
-------------------
START: After entering your name and selecting an avatar, press ENTER.

BATTLE:
1 - Attack (random value between 15–25)
2 - Heal (random value between 10–20)
3 - Pass (skip turn)

END SCREEN: Press ESC to exit the game.

-------------------
Have fun!