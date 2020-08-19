# MacGyver Escape

MacGyver Escape is a small 2D game coded in Python with PyGame library.

To win : collect three objects randomly in the labyrinth (needle, ether and plastic tube) to craft a syringe and put the guard to sleep. It's the only way to escape.

Script: Python

Files:
- classes/ (modules)
    - locale.py (constants)
    - entity.py (character and item)
    - map.py (map reader)
    - window.py (initialisation and window refresh)
- resource/ (images)
- map (labyrinth structure)



To clone and play to this game, you must follow these instructions :
```git clone https://github.com/RiwsPy/MacGyver.git
cd MacGyver/
pipenv install
pipenv shell
python3 main.py
```

See the **Pipfile.lock** for more details on dependies.




# Credits
- PyGame library
- Olivier Elophe (for advise)