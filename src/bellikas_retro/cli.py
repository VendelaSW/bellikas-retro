def main():
    import inspect
    from streamlit.web import cli as stcli
    import bellikas_retro.app as app

    app_path = inspect.getfile(app)
    stcli.main(["run", app_path])