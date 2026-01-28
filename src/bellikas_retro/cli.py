def main():
    import inspect
    import os
    #from streamlit.web import cli as stcli
    from . import app

    app_path = inspect.getfile(app)
    #stcli.main(["run", app_path])
    os.system("python -m streamlit run", app_path)
