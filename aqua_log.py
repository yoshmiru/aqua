from logging import Formatter, DEBUG
from logging.handlers import RotatingFileHandler

def logHandler():
    handler = RotatingFileHandler('aqua.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    return handler


def setup(app):
    # logger settings
    app.logger.setLevel(DEBUG)
    app.logger.addHandler(logHandler())
    return app.logger
