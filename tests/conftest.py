import pytest

@pytest.fixture(autouse=True)
def dataset_fixture(tmp_path, monkeypatch):
    monkeypatch.setenv("SKIP_DATA_DOWNLOAD", "1")

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    (data_dir / "vgsales.csv").write_text(
        "Rank,Name,Platform,Year,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales\n"
        "1,TestGame,PS2,2001,2.0,1.0,0.1,0.2,3.3\n"
    )

    # Patch config constant
    import bellikas_retro.utils.config as config
    monkeypatch.setattr(config, "DATA_DIR", data_dir, raising=True)

    # Patch the already-imported copy inside app_state
    import bellikas_retro.app_state as app_state
    monkeypatch.setattr(app_state, "DATA_DIR", data_dir, raising=True)
