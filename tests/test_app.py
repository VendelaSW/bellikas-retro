from streamlit.testing.v1 import AppTest
from bellikas_retro.utils import PROJECT_ROOT
from pathlib import Path
import pytest

# Test for age input in nostalgia
def test_age_increments():
    nostalgia_path = (PROJECT_ROOT / "src" / "bellikas_retro" / "pages" / "nostalgia.py").resolve()

    assert nostalgia_path.is_file(), f"nostalgia.py not found at: {nostalgia_path}"

    at = AppTest.from_file(str(nostalgia_path)).run()
    assert not at.exception

    start_age = 25
    at.number_input("nostalgia_age").set_value(start_age).run()
    assert not at.exception
    assert at.number_input("nostalgia_age").value == start_age

    at.number_input("nostalgia_age").set_value(start_age + 1).run()
    assert not at.exception
    assert at.number_input("nostalgia_age").value == start_age + 1

def test_age_rejects_letters():
    # Path to the Nostalgia page
    nostalgia_path = (PROJECT_ROOT / "src" / "bellikas_retro" / "pages" / "nostalgia.py").resolve()
    assert nostalgia_path.is_file(), f"nostalgia.py not found at: {nostalgia_path}"

    # Launch page in test mode
    at = AppTest.from_file(str(nostalgia_path)).run()
    assert not at.exception, "Page crashed on launch"

    # Try entering a letter into the age number input
    invalid_age = "a"

    with pytest.raises(Exception) as exc_info:
        at.number_input("nostalgia_age").set_value(invalid_age).run()

    assert "must be real number, not str" in str(exc_info.value)

def test_pages_load():

    PAGES = ["home.py", "nostalgia.py", "top.py", "charts.py"]
    BASE_PATH = Path(__file__).parent.parent / "src" / "bellikas_retro" / "pages"
    """Ensure all pages load without exceptions."""
    for page_file in PAGES:
        page_path = BASE_PATH / page_file
        assert page_path.is_file(), f"{page_file} not found at {page_path}"

        # Load and run the page
        at = AppTest.from_file(str(page_path)).run()

        # Make sure there were no exceptions
        assert not at.exception, f"Page {page_file} failed to load: {at.exception}"
