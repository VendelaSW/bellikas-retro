from streamlit.testing.v1 import AppTest
from bellikas_retro.utils import PROJECT_ROOT

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
