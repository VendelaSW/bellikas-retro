from streamlit.testing.v1 import AppTest
from bellikas_retro.utils import PROJECT_ROOT


def test_age_increments():
    app_path = (PROJECT_ROOT / "src" / "bellikas_retro" / "app.py").resolve()

    assert app_path.is_file(), f"app.py not found at: {app_path}"

    at = AppTest.from_file(str(app_path)).run()
    assert not at.exception

    start_age = 25
    at.number_input("age").set_value(start_age).run()
    assert not at.exception
    assert at.number_input("age").value == start_age

    at.number_input("age").set_value(start_age + 1).run()
    assert not at.exception
    assert at.number_input("age").value == start_age + 1
