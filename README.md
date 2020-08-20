# MacGyver Escape

MacGyver Escape is a small 2D game coded in Python with PyGame library.

To win : collect three objects randomly in the labyrinth (needle, ether and plastic tube) to craft a syringe and put the guard to sleep. It's the only way to escape.

Script: Python

Files:
- config/
    - locale.py (constants)
- data/
    - map_01.txt (labyrinth structure)
- game/ (modules)
    - entity.py (character and items)
    - map.py (map loader)
    - window.py (initialisation and window refresh)
- resource/ (images)
- main.py
- Pipfile.lock
- README.md


To clone and play to this game, you must follow these instructions :
```
git clone https://github.com/RiwsPy/MacGyver.git
cd MacGyver/
pipenv install
pipenv shell
python3 main.py
```

See the **Pipfile.lock** for more details on dependies.




# Credits
- PyGame library
- Olivier Elophe (for advise)