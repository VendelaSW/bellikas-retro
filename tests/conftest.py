import pytest


@pytest.fixture(autouse=True)
def dataset_fixture(tmp_path, monkeypatch):
    # Ensure CI never tries to download
    monkeypatch.setenv("SKIP_DATA_DOWNLOAD", "1")

    monkeypatch.chdir(tmp_path)

    data_dir = tmp_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    # Create fake data for testing
    (data_dir / "vgsales.csv").write_text(
        "Rank,Name,Platform,Year,NA_Sales,EU_Sales,JP_Sales,Other_Sales,Global_Sales\n"
        "1,TestGame,PS2,2001,2.0,1.0,0.1,0.2,3.3\n"
    )
