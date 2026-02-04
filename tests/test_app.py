from streamlit.testing.v1 import AppTest
from bellikas_retro.utils import PROJECT_ROOT

# Test for age input in charts
def test_age_increments():
    charts_path = (PROJECT_ROOT / "src" / "bellikas_retro" / "pages" / "charts.py").resolve()

    assert charts_path.is_file(), f"charts.py not found at: {charts_path}"

    at = AppTest.from_file(str(charts_path)).run()
    assert not at.exception

    start_age = 25
    at.number_input("charts_age").set_value(start_age).run()
    assert not at.exception
    assert at.number_input("charts_age").value == start_age

    at.number_input("charts_age").set_value(start_age + 1).run()
    assert not at.exception
    assert at.number_input("charts_age").value == start_age + 1
