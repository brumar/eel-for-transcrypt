// Transcrypt'ed from Python, 2018-12-06 23:16:09
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {InventoryItem} from './web.common.js';
import {dataclass} from './dataclasses.js';
var __name__ = '__main__';
export var applyfact = function (inputfactory, outputfactory) {
	if (typeof inputfactory == 'undefined' || (inputfactory != null && inputfactory.hasOwnProperty ("__kwargtrans__"))) {;
		var inputfactory = null;
	};
	if (typeof outputfactory == 'undefined' || (outputfactory != null && outputfactory.hasOwnProperty ("__kwargtrans__"))) {;
		var outputfactory = null;
	};
	var applyfact_inside = function (func) {
		var newfunction = function () {
			var kwargs = dict ();
			if (arguments.length) {
				var __ilastarg0__ = arguments.length - 1;
				if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
					var __allkwargs0__ = arguments [__ilastarg0__--];
					for (var __attrib0__ in __allkwargs0__) {
						switch (__attrib0__) {
							default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
						}
					}
					delete kwargs.__kwargtrans__;
				}
				var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
			}
			else {
				var args = tuple ();
			}
			if (inputfactory !== null) {
				if (outputfactory !== null) {
					return outputfactory (func (inputfactory (...args, __kwargtrans__ (kwargs))));
				}
				else {
					return func (inputfactory (...args, __kwargtrans__ (kwargs)));
				}
			}
			else if (outputfactory !== null) {
				try {
					outputfactory (func (__kwargtrans__ (args [0] [0])));
				}
				catch (__except0__) {
					return outputfactory (func (...args, __kwargtrans__ (kwargs)));
				}
			}
			else {
				return func (...args, __kwargtrans__ (kwargs));
			}
		};
		return newfunction;
	};
	return applyfact_inside;
};
export var identity_js = function (anything) {
	return anything;
};
export var identity_caller = async function (anything) {
	var v = await backend_pytest.i_return_the_same (anything) ();
	return v;
};
export var transcrypt_generator = function* (mn, mx) {
	for (var v = mn; v < mx; v++) {
		yield v;
	}
	};
export var call_a_python_generator_from_js = async function (mn, mx) {
	var v = await backend_pytest.a_generator (mn, mx) ();
	return v;
};
export var get_a_dataclass = applyfact (__kwargtrans__ ({outputfactory: InventoryItem})) (async function (strg, flt, intval) {
	var d = await backend_pytest.return_a_dataclass (strg, flt, intval) ();
	return d;
});
Object.defineProperty(get_a_dataclass, "name", { value: "get_a_dataclass" });
export var build_send_getback_a_dataclass = applyfact (__kwargtrans__ ({outputfactory: InventoryItem})) (async function (strg, flt, intval) {
	var dc = InventoryItem (strg, flt, intval);
	var d = await backend_pytest.return_a_dataclass (dc) ();
	return d;
});
Object.defineProperty(build_send_getback_a_dataclass, "name", { value: "build_send_getback_a_dataclass" });
export var accept_a_dataclass = applyfact (__kwargtrans__ ({outputfactory: InventoryItem})) (async function () {
	var kwargs = dict ();
	if (arguments.length) {
		var __ilastarg0__ = arguments.length - 1;
		if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
			var __allkwargs0__ = arguments [__ilastarg0__--];
			for (var __attrib0__ in __allkwargs0__) {
				switch (__attrib0__) {
					default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
				}
			}
			delete kwargs.__kwargtrans__;
		}
		var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
	}
	else {
		var args = tuple ();
	}
	var dc = args [0];
	var d = await backend_pytest.return_a_dataclass (dc) ();
	return d;
});
Object.defineProperty(accept_a_dataclass, "name", { value: "accept_a_dataclass" });

//# sourceMappingURL=tests.map