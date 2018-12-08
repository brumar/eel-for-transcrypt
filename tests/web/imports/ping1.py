import eel_for_transcrypt as eel

with eel.import_frontend_functions():
    from web.imports.pong1 import pongball
    

@eel.expose
def pingball(counter):
    counter += 1
    if counter < 50:
        return pongball(counter)()
    else:
        return counter
