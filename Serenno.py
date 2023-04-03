from adsk.core import Application
from .init import listener

def run(context: dict):
    app = Application.get()
    listener.init(app)
