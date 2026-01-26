Client Request: Bellika’s Retro

Bellika is opening a retro gaming store and wants to make data-driven decisions about which games to stock. To support this, he has requested historical video game sales data to identify titles that were popular in the past. Additionally, he is aware that the average gamer today is 36 years old, meaning games from that generation’s childhood are likely to be especially appealing to his target audience.
``` html
    root/
├── src/
│   └── bellikas_retro/
│       ├── __init__.py
│       ├── app.py
│       ├── cli.py
│       ├── games/
│       │   ├── __init__.py
│       │   ├── game.py
│       │   └── game_collection.py
│       ├── data_loader/
│       │   ├── __init__.py
│       │   ├── loader.py
│       │   └── downloader.py
│       └── utils/
│           ├── __init__.py
│           ├── logger.py
│           └── config.py
├── tests/
│   └── ...
├── data/
├── logs/
├── .github/
│   └── workflows/
│       └── tests.yml
├── pyproject.toml
├── README.md
└── .gitignore
