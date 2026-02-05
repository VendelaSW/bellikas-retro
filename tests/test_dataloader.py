from pathlib import Path
from bellikas_retro.data_loader.data_loader import DataLoader   

def test_dataloader_loads_csv(tmp_path: Path):
    (tmp_path / "vgsales.csv").write_text(
        "Name,Platform,Year,Genre\nGame A,Wii,2008,Action\n",
        encoding="utf-8",
    )

    loader = DataLoader(data_dir=tmp_path)
    df = loader.load()

    assert len(df) == 1
