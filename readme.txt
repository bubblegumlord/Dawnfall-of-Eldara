====================
 DAWNFALL OF ELDARA
====================

Opis:
-------------------
"Dawnfall of Eldara" to prosty dungeon crawler stworzony na wzór klasycznych turowych gier RPG typu Final Fantasy lub Might and Magic. 4 graczy tworzy drużynę bohaterów, którzy wspólnie eksplorują lochy Eldary. Gracze wykonują odpowiednie akcje pokonując kolejnych przeciwników, aby odkryć ukryty skarb, unikając przy tym własnej zguby. 

Projekt stworzony na zajęcia Programowanie aplikacji klient-serwer.

Wymagania:
-------------------
- Python 3.9 lub nowszy
- Pygame 2.0 lub nowszy

Struktura:
-------------------
- server.py     - uruchamia serwer gry 
- client.py     - uruchamia klienta 
- game/         - logika gry 
- ui/           - ekrany gry, funkcje związane z GUI 
- assets/       - grafiki, czcionki, tła 

Uruchomienie:
-------------------
1. W pierwszym terminalu:
    python server.py

2. W 4 następnych terminalach:
    python client.py

Gracze dołączają do serwera aż utworzy się pełna drużyna z 4 osób — gra rozpocznie się automatycznie.

Sterowanie:
-------------------
START: Po wpisaniu imienia i wyborze awatara nacisnąć ENTER.
WALKA:
1 - Atak (wartość losowa 15-25)
2 - Ulecz (wartość losowa 10-20)
3 - Pas (pominięcie kolejki)
EKRAN KOŃCOWY: ESC, aby wyjść z gry.

-------------------
Miłej zabawy!
