from __future__ import print_function
import gevent as gvt
import gevent.monkey as mky; mky.patch_all()
from builtins import range
from io import open
import json as jsn
import bottle as btl
import bottle.ext.websocket as wbs
import re as rgx
import os
import eel_for_transcrypt.browsers as brw
import random as rnd
import sys
import pkg_resources as pkg
import socket
import contextlib
import importlib
import pkgutil
from collections import defaultdict
from functools import partial
import copy
import unittest
import types
import logging
import dataclasses
from functools import wraps
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

#logger = logging.getLogger("eel")


TIME_OUT = 10  # seconds
_eel_js_file = pkg.resource_filename('eel_for_transcrypt', 'eel.js')
_eel_js = open(_eel_js_file, encoding='utf-8').read()
_websockets = []
_message_loop_queue = []
_call_return_values = {}
_call_return_callbacks = {}
_call_number = 0
_exposed_functions = {}
_js_functions = []
_start_geometry = {}
_mock_queue = []
_mock_queue_done = set()
_on_close_callback = None
_default_options = {
    'mode': 'chrome-app',
    'host': 'localhost',
    'port': 8000,
    'chromeFlags': []
}
frontend_modules = defaultdict(set)

NEEDED_PY_FUNCTIONS = []
BACKEND_NAMES = []
FRONTEND_FILES = []
OTHER_IMPORTS = []

import contextlib
import builtins

#EEL_MAGIC_MOCK = MagicMock()

import re


def notcommented(line):
    for car in line:
        if car == "#":
            return False
        if not car.isspace():
            return True



def find_exposed_transcrypt_functions(filepath, caller):
    regex = caller+"\.([^(]+)\("
    with open(filepath, "r") as f:
        vlist = [line.strip() for line in f if notcommented(line)]
        for match in re.finditer(regex, "".join(vlist), re.MULTILINE):
            function_name = match.group(1)
            expose(function_name)


def search_in_import(strval):
    l = pkgutil.get_loader("web.frontendscrypt")
    return l.path


def add_to_callers(caller, strval):
    frontend_modules[strval].add(caller)

def jscaller(*args, **kwargs):
    name = kwargs.pop("name")
    arglist = list(kwargs.values()) + list(args)
    return _js_call(name, arglist)

# Public functions
def new_import(old_import):
    """block import from frontend. Instead, alias the function to eel._js_call(functionname) 
    and redirect the import so that this is the function that is really imported"""
    # Internally, python may import things at unexpected moment
    # so be very careful to be wary when adding code in this part
    # because everything that will be imported, will use our patch
    # instead of the real importer
    def new_new_import(strval, globs, locs, alist, anumber):
        #logging.info(f"attempt to import from frontend: {strval}, {alist}")
        global OTHER_IMPORTS
        global FRONTEND_FILES
        OTHER_IMPORTS.append((strval,globs, locs, alist, anumber))
        if strval == 'shutil':
            # very important to keep this, because the debugging session in pytest
            # import this on the fly, which can create hell on earth because this
            # code will mock out large part of stlib and loop forerver
            return old_import(strval, globs, locs, alist, anumber)
        if alist is not None:
            for imported_function in alist:
                _mock_js_function(imported_function)
                f = partial(jscaller, name=imported_function)
                setattr(sys.modules[__name__], imported_function, f)
                _js_functions.append(imported_function)
            return old_import("eel_for_transcrypt", globs, locs, alist, anumber)
        else:
            raise Exception("You must write your imports under the 'form from x.y import z'")
    return new_new_import





def new_import_backend(old_import):
    """block specific import from backend. Instead, alias the function to eel._js_call(functionname)
    and redirect the import so that this is the function that is really imported. The backend itself will be
    imported after this redirection"""
    # Internally, python may import things at unexpected moment
    # so be very careful to be wary when adding code in this part
    # even printing and loging should be forbidden as they import things
    # because everything that will be imported, will use our patch
    # instead of the real importer
    def new_new_back_import(strval, globs, locs, alist, anumber):
        #logging.info(f"block the backend import {strval} {alist}")
        #logging.info(strval, alist)
        global BACKEND_NAMES
        if strval == 'shutil':
            # very important to keep this, because the debugging session in pytest
            # import this on the fly, which can create hell on earth because this
            # code will mock out large part of stlib and loop forerver
            return old_import(strval, globs, locs, alist, anumber)
        if strval not in BACKEND_NAMES:
            BACKEND_NAMES.append(strval)
        if alist:
            sys.modules["__sink"] = unittest.mock.MagicMock()
            return old_import("__sink", globs, locs, alist, anumber)
        else:
            sys.modules["__sink"] = unittest.mock.MagicMock()
            return old_import("__sink", globs, locs, None, anumber)
    return new_new_back_import

@contextlib.contextmanager
def import_frontend_functions():
    """
    Patch the python import mechanism for frontend functions
    """
    global pre_patched_value
    pre_patched_value = copy.deepcopy(builtins.__import__)
    builtins.__import__ = new_import(pre_patched_value)
    logging.info("enter frontend patching")
    yield "done"
    logging.info("leaving frontend patching")
    builtins.__import__ = pre_patched_value
    while(OTHER_IMPORTS):
        strval, globs, locs, alist, anumber = OTHER_IMPORTS.pop()
        logging.info(f"simple backend import {strval}")
        __import__(strval, globs, locs, None, anumber)
        

@contextlib.contextmanager
def import_backend_modules(already_imported):
    """
    Patch the python import mechanism for frontend functions
    """
    if already_imported:
        global pre_patched_value
        pre_patched_value = copy.deepcopy(builtins.__import__)
        builtins.__import__ = new_import_backend(pre_patched_value)
        logging.info("enter frontend patching")
        yield "done"
        logging.info("leaving frontend patching")
        builtins.__import__ = pre_patched_value
        import_frontend_functions
    else:
        yield "DONE"


def apply_factories(inputfactory=None, outputfactory=None):
    def new_decorator(func):
        @wraps(func)  # so that the function keep its name
        def newfunction(*args, **kwargs):
            if inputfactory is not None:
                if outputfactory is not None:
                    return outputfactory(func(inputfactory(*args, **kwargs)))
                else:
                    if isinstance(args[0], dict):
                        return func(inputfactory(**args[0]))
                    else:
                        return func(inputfactory(*args, **kwargs))
            else:
                if outputfactory is not None:
                    return outputfactory(func(*args, **kwargs))
                else:
                    return func(*args, **kwargs)
        return newfunction
    
    return new_decorator
    

def expose(name_or_function=None,
           outputfactory=None,
           inputfactory=None):
    # Deal with '@eel.expose()' - treat as '@eel.expose'
    if name_or_function is None:
        return expose

    if type(name_or_function) == str:   # Called as '@eel.expose("my_name")'
        name = name_or_function

        def decorator(function):
            _expose(name, function)
            return function
        return decorator
    else:
        _expose(name_or_function.__name__, name_or_function)
        return name_or_function


def init(path, search_exposed_js=True, search_into_imports=False):
    global root_path
    root_path = _get_real_path(path)
    if search_exposed_js:
        js_functions = search_in_static_files(root_path)
    
        _js_functions = list(js_functions)
        for js_function in _js_functions:
            _mock_js_function(js_function)
    if search_into_imports:
        for frontend_module, callers_set in frontend_modules.items():
            module_filepath = search_in_import(frontend_module)
            for caller in callers_set:
                find_exposed_transcrypt_functions(module_filepath, caller=caller)
            
    
def register_backend_names(listofnames):
    global BACKEND_NAMES
    BACKEND_NAMES = listofnames

def register_frontend_js_files(filepathlist):
    global FRONTEND_FILES
    FRONTEND_FILES = filepathlist


def build_autobridgejs():
    lines = []
    for backend_name in BACKEND_NAMES:
        lines.append(f"window.{backend_name} = eel;")
    for frontfilepath in FRONTEND_FILES:
        if frontfilepath.startswith("./web/"):
            frontfilepath = frontfilepath.replace("./web/", "./")
        if frontfilepath.startswith("./web"):
            frontfilepath = frontfilepath.replace("./web", "./")
        if frontfilepath.startswith("/web"):
            frontfilepath = frontfilepath.replace("/web", "./")
        if frontfilepath.startswith("web"):
            frontfilepath = frontfilepath.replace("web/", "./")
        module_name = frontfilepath.split("/")[-1].split(".")[0]
        lines.append(f"import * as {module_name} from '{frontfilepath}';")
        lines.append(f"window.{module_name} = {module_name};")
        lines.append(f"var functions = Object.keys({module_name})")
        lines.append("for (var i=0; i < functions.length; i++){")
        lines.append("    var name = functions[i];")
        #lines.append(f"    if ({module_name}[functions[i]].py_name !== undefined)"+ ' {')
        #lines.append(f"        name = {module_name}[functions[i]].py_name" + "}")
        lines.append(f"eel.expose({module_name}[functions[i]], name);")
        lines.append("}")
    return "\r\n".join(lines)
        
    
def search_in_static_files(root_path):
    js_functions = set()
    for root, _, files in os.walk(root_path):
        for name in files:
            allowed_extensions = '.js .html .txt .htm .xhtml'.split()
            if not any(name.endswith(ext) for ext in allowed_extensions):
                continue
            
            try:
                with open(os.path.join(root, name), encoding='utf-8') as file:
                    contents = file.read()
                    expose_calls = set()
                    finder = rgx.findall(r'eel\.expose\((.*)\)', contents)
                    for expose_call in finder:
                        expose_call = expose_call.strip()
                        msg = "eel.expose() call contains '(' or '='"
                        assert rgx.findall(
                            r'[\(=]', expose_call) == [], msg
                        expose_calls.add(expose_call)
                    js_functions.update(expose_calls)
            except UnicodeDecodeError:
                pass  # Malformed file probably
    return js_functions


def start(*start_urls, **kwargs):
    global _on_close_callback

    block = kwargs.pop('block', True)
    options = kwargs.pop('options', {})
    size = kwargs.pop('size', None)
    position = kwargs.pop('position', None)
    geometry = kwargs.pop('geometry', {})
    _on_close_callback = kwargs.pop('callback', None)
    bottle_already_started = kwargs.pop('alive', False)

    for k, v in list(_default_options.items()):
        if k not in options:
            options[k] = v

    _start_geometry['default'] = {'size': size, 'position': position}
    _start_geometry['pages'] = geometry

    if options['port'] == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        options['port'] = sock.getsockname()[1]
        sock.close()
    
    if not bottle_already_started:
        brw.open(start_urls, options)
        def run_lambda():
            return btl.run(
                host=options['host'],
                port=options['port'],
                server=wbs.GeventWebSocketServer,
                debug=False,
                quiet=False)
        if block:
            run_lambda()
        else:
            spawn(run_lambda)


def sleep(seconds):
    gvt.sleep(seconds)

def set_timeout(timeout):
    global TIME_OUT
    TIME_OUT = timeout

def spawn(function, *args, **kwargs):
    gvt.spawn(function, *args, **kwargs)

# Bottle Routes

@btl.route('/eel.js')
def _eel():
    funcs = list(_exposed_functions.keys())
    page = _eel_js.replace('/** _py_functions **/',
                           '_py_functions: %s,' % funcs)
    page = page.replace('/** _start_geometry **/',
                        '_start_geometry: %s,' % jsn.dumps(_start_geometry))
    btl.response.content_type = 'application/javascript'
    return page

@btl.route('/autobridge.js')
def _bridge():
    page = build_autobridgejs()
    btl.response.content_type = 'application/javascript'
    return page


@btl.route('/<path:path>')
def _static(path):
    return btl.static_file(path, root=root_path)


@btl.get('/eel', apply=[wbs.websocket])
def _websocket(ws):
    global _websockets
    global _message_loop_queue
    
    for js_function in _js_functions:
        _import_js_function(js_function)

    page = btl.request.query.page
    if page not in _mock_queue_done:
        for call in _mock_queue:
            _repeated_send(ws, eel_json_dumps(call))
        _mock_queue_done.add(page)

    _websockets += [(page, ws)]

    while True:
        msg = ws.receive()
        if msg is not None:
            message = jsn.loads(msg)
            spawn(_process_message, message, ws)
        else:
            _websockets.remove((page, ws))
            break

    _websocket_close(page)

# Private functions

def _repeated_send(ws, msg):
    for attempt in range(100):
        try:
            ws.send(msg)
            break
        except Exception as e:
            logging.exception("exception")
            sleep(0.001)
    else:
        logging.error(f"unable to send this message {str(msg)}")
        _debug_health_check()

accumulators = defaultdict(list)

def call_debug_eel():
    for _, ws in _websockets:
        _repeated_send(ws, eel_json_dumps({  'debug': "debug",
                                    'value': return_val}))
    


def _process_message(message, ws):
    global accumulators
    if 'call' in message:
        # from python to js
        return_val = _exposed_functions[message['name']](*message['args'])
        # IMPORTANT listing values from python generator provoques
        # a blocking type. One should better use accumulator like in the js side
        if isinstance(return_val, types.GeneratorType):
            previous_result = next(return_val);
            iterator_ended = False
            while not iterator_ended :
                try:
                    result = next(return_val)
                except StopIteration:
                    iterator_ended = True
                finally:
                    _repeated_send(ws, eel_json_dumps({'return': message["call"],
                                                    'value': previous_result,
                                                     'continue': not iterator_ended}));
                previous_result = result
        else:
            _repeated_send(ws, eel_json_dumps({  'return': message['call'],
                                        'value': return_val    }))
    elif 'return' in message:
        # from js to python
        call_id = message['return']
        generator = "continue" in message.keys()
        docontinue = generator and message["continue"]!=False
        if call_id in _call_return_callbacks:
            if not docontinue:
                callback = _call_return_callbacks.pop(call_id)
                if not generator:
                    # the last value of a generator is None
                    # and should not be sent back 
                    callback(message["value"])
            else:
                callback = _call_return_callbacks[call_id]
                callback(message['value'])
        else:
            # todo => checkifthis works in eelcloned
            # check if it blocks everything or not
            if generator:
                if docontinue:
                    accumulators[call_id].append(message["value"])
                else:
                    _call_return_values[call_id] = accumulators.pop(call_id)
            else:
                _call_return_values[call_id] = message["value"]
    else:
        logging.error('Invalid message received: ', message)
        _debug_health_check()


def _get_real_path(path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, path)
    else:
        return os.path.abspath(path)


def _mock_js_function(f):
    # f = f.split(',')[0],
    # allow to use eel.expose(func, name) in js and only take func
    # this is fix commented out because a better solution has been found, cf current commit eel.js

    exec('%s = lambda *args: _mock_call("%s", args)' % (f, f), globals())


def _import_js_function(f):
    # f = f.split(',')[0]
    # allow to use eel.expose(func, name) in js and only take func
    # this is fix commented out because a better solution has been found, cf current commit eel.js
    exec('%s = lambda *args: _js_call("%s", args)' % (f, f), globals())


def _call_object(name, args):
    global _call_number
    _call_number += 1
    call_id = _call_number + rnd.random()
    return {'call': call_id, 'name': name, 'args': args}


def _mock_call(name, args):
    call_object = _call_object(name, args)
    global _mock_queue
    _mock_queue += [call_object]
    return _call_return(call_object)


def _js_call(name, args):
    #logging.info("js call")
    #logging.info(name, args)
    call_object = _call_object(name, args)
    for _, ws in _websockets:
        _repeated_send(ws, eel_json_dumps(call_object))
    return _call_return(call_object)


def _call_return(call):
    call_id = call['call']

    def return_func(callback=None):
        if callback is not None:
            _call_return_callbacks[call_id] = callback
        else:
            index = 0
            while True:
                if call_id in _call_return_values:
                    return _call_return_values.pop(call_id)
                sleep(0.001)
                index += 0.001
                if index >= TIME_OUT:
                    logging.error(f"timed out. No answer from javascript. call_id {call_id}")
                    break
    return return_func


def _expose(name, function):
    if name in _exposed_functions:
        raise Exception(f"Already exposed function with name {name}")
    _exposed_functions[name] = function


def _websocket_close(page):
    logging.error("sockets unresponsive. The system would like to exit")
    _debug_health_check()
    if _on_close_callback is not None:
        sockets = [p for _, p in _websockets]
        _on_close_callback(page, sockets)
        logging.warning("_on_close_callback is called")
    else:
        sleep(1.0)
        if len(_websockets) == 0:
            logging.error("The system has exited")
            sys.exit()

def _debug_health_check():
    logging.info("list of python exposed function")
    for f in _exposed_functions:
        logging.info(f"    {f}")
    logging.info("list of known js functions")
    for f in _js_functions:
        logging.info(f"    {f}")
    logging.info("list of known BACKEND Files")
    for b in BACKEND_NAMES:
        logging.info(f"    {b}")
    logging.info("list of known FRONT END Files")
    for f in FRONTEND_FILES:
        logging.info(f"    {f}")
    #v = _js_call("_debug",tuple("debug"))()
    #logging.info(v)
    
class EelJSONEncoder(jsn.JSONEncoder):
        def default(self, o):
            if dataclasses.is_dataclass(o):
                return dataclasses.asdict(o)
            return super().default(o)


def eel_json_dumps(target):
    return jsn.dumps(target, cls=EelJSONEncoder)

