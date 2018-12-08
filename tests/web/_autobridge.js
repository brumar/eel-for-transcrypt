// THIS COULD BE GENERATED
// backend => name of backend
// frontend => same
window.backend = eel; //for each backend

//for each frontend
import * as front from './__target__/frontendscrypt.js';
window.front = front;
var functions = Object.keys(front)
for (var i=0; i < functions.length; i++){
        eel.expose(front[functions[i]], functions[i]);
    }
// exposing all the front functions is harmless
// because they also need to be imported in the backend to be used
