import eel_for_transcrypt as eel

with eel.import_frontend_functions():
    from web.anotherfrontend import biglogger
    

@eel.expose
def substract(a, b):
    val = a - b
    biglogger("this is something")
    biglogger(val)
    return val
