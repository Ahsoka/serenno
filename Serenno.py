from adsk.core import Application
from .init import listener

def run(context: dict):
    app = Application.get()
    listener.init(app)

def stop(context: dict):
    # TODO: Added error handling in the stop function;
    # any errors that happen here are not recorded on the console
    listener.destroy()
