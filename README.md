# Bellika's Retro

[![Python][ico-python]][link-python]
[![Streamlit][ico-streamlit]][link-streamlit]
[![Dataset][ico-kaggle]][link-kaggle]
[![GitHub][ico-github]][link-github-org]

This is where your description should go. Try and limit it to a paragraph or two, and maybe throw in a mention of what
PSRs you support to avoid any confusion with users and contributors.

## Structure

If any of the following are applicable to your project, then the directory structure should follow industry best practices by being named the following.

```
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
```

## Install

**1. Create and activate a virtual environment:**

```bash
python -m venv .venv
source .venv/bin/activate (POSIX)
source .venv/Scripts/activate (Windows)
```

**2. Install the project:**

```bash
pip install -e .
```

## Usage

**Run:**

```bash
bellikas_retro
```

**Run as a module:**

```bash
python -m bellikas_retro
```

**Uninstall the project:**
```bash
pip uninstall bellikas_retro
```

## Change log

Please see [CHANGELOG](CHANGELOG.md) for more information on what has changed recently.

## Testing

``` bash
$ composer test
```

## Contributing

Please see [CONTRIBUTING](CONTRIBUTING.md) and [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) for details.

## Security

If you discover any security related issues, please email :author_email instead of using the issue tracker.

## Credits

- [:author_name][link-author]
- [All Contributors][link-contributors]

## License

# Python
[ico-python]: https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white
[link-python]: https://www.python.org/

# Streamlit
[ico-streamlit]: https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white
[link-streamlit]: https://streamlit.io/

# Kaggle dataset
[ico-kaggle]: https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle&logoColor=white
[link-kaggle]: https://www.kaggle.com/datasets/gregorut/videogamesales

# GitHub
[ico-github]: https://img.shields.io/badge/GitHub-Contributors-black?logo=github
[link-github-org]: https://github.com/VendelaSW/bellikas-retro