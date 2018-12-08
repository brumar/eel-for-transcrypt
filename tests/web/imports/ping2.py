import eel_for_transcrypt as eel

with eel.import_frontend_functions():
    from web.imports.pong2 import pingball
    

@eel.expose
def ping2(counter):
    counter += 1
    if counter < 50:
        return pingball(counter)
    else:
        return counter
