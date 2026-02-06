# Bellika's Retro

<p>
  <a href="https://www.python.org/" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt=""></a>&nbsp;&nbsp;&nbsp;
    
  <a href="https://streamlit.io/" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Streamlit-App-red?logo=streamlit&logoColor=white" alt=""></a>&nbsp;&nbsp;&nbsp;
  
  <a href="https://www.kaggle.com/datasets/gregorut/videogamesales" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/Dataset-Kaggle-20BEFF?logo=kaggle&logoColor=white" alt=""></a>&nbsp;&nbsp;&nbsp;

  <a href="https://github.com/VendelaSW/bellikas-retro/actions/workflows/ci.yml">
  <img src="https://github.com/VendelaSW/bellikas-retro/actions/workflows/ci.yml/badge.svg?branch=main" alt="CI status">
  </a>&nbsp;&nbsp;&nbsp;
  
  <a href="https://github.com/VendelaSW/bellikas-retro" target="_blank" rel="noopener noreferrer">
  <img src="https://img.shields.io/badge/GitHub-Contributors-black?logo=github" alt=""></a>
</p>

Transforms video game sales data into clear insights, revealing retro titles that resonate with different age groups.  
Based on release year, platform, and copies sold, the results are presented through clear and intuitive visualizations.

## Structure

```
    root/
├── src/
│   └── bellikas_retro/
│       ├── data_loader/        # Data downloading and loading logic
│       │   ├── __init__.py
│       │   ├── data_loader.py
│       │   └── downloader.py
│       ├── pages/              # Streamlit pages and visual views
│       │   ├── charts.py
│       │   ├── home.py
│       │   ├── nostalgia.py
│       │   └── top.py
│       ├── static/             # Static assets (images, media, etc.)
│       │   ├── neonsign.png
│       └── utils/              # Shared utilities, configuration, and validation
│           ├── __init__.py
│           ├── config.py
│           ├── helpers.py
│           ├── logger.py
│           └── validations.py
│       ├── __init__.py
│       ├── app_state.py        # Application state management
│       ├── app.py              # Main application entry point
│       ├── cli.py              # Command-line interface
├── tests/                      # Automated tests
│   └── test_app.py
├── pyproject.toml              # Project configuration and dependencies
└── README.md
```
The project follows a modular and scalable structure, clearly separating data handling, application logic, user interface, and utilities.  
This design improves readability, supports collaboration, and makes the codebase easy to maintain and extend as new features are added.

## CI/CD

GitHub Actions runs automated tests and build checks on every push and pull request to `dev` and `main`.

Pipeline includes:
- Environment validation (`SKIP_DATA_DOWNLOAD=1`)
- Test matrix (Python 3.10–3.13)
- Package build sanity check

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

This starts the Streamlit application in your browser.

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


## Testing

**Run all tests locally:**

``` bash
pytest
```

**Verbose output:**

``` bash
pytest -v
```

**Quiet output:**

``` bash
pytest -q
```

## Credits

- [VendelaSW](https://github.com/VendelaSW) — project author  
- All contributors: https://github.com/VendelaSW/bellikas-retro/graphs/contributors

**Responsibilities:**

[VendelaSW](https://github.com/VendelaSW): Streamlit frontend, UX, charts, validations, deployment

[VWiman](https://github.com/VWiman): Backend, CI/CD, testing infrastructure, integration, Scrum

[emmykristina](https://github.com/emmykristina): UI design, CSS, validations, documentation

[folixd](https://github.com/folixd): Logging system, early testing and code quality practices

[kevin3169](https://github.com/kevin3169): Helpers, thresholds, dataloader tests 

## License

MIT License — see [LICENSE](LICENSE)
