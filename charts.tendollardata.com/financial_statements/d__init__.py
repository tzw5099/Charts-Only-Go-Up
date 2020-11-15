# https://flask.palletsprojects.com/en/1.1.x/tutorial/views/
def create_app():
    app = ...
    # existing code omitted

    from . import palletauth
    app.register_blueprint(auth.bp)

    return app
