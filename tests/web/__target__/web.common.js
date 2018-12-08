// Transcrypt'ed from Python, 2018-12-06 23:16:09
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
import {dataclass} from './dataclasses.js';
var __name__ = 'web.common';
export var InventoryItem =  __class__ ('InventoryItem', [object], {
	__module__: __name__,
	get __init__ () {return __get__ (this, function (self) {
		var kwargs = dict ();
		if (arguments.length) {
			var __ilastarg0__ = arguments.length - 1;
			if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
				var __allkwargs0__ = arguments [__ilastarg0__--];
				for (var __attrib0__ in __allkwargs0__) {
					switch (__attrib0__) {
						case 'self': var self = __allkwargs0__ [__attrib0__]; break;
						default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
					}
				}
				delete kwargs.__kwargtrans__;
			}
			var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
		}
		else {
			var args = tuple ();
		}
		let names = self.__initfields__.values ();
		for (let arg of args) {
		    self [names.next () .value] = arg;
		}
		for (let name of kwargs.py_keys ()) {
		    self [name] = kwargs [name];
		}
	});},
	get __repr__ () {return __get__ (this, function (self) {
		let names = self.__reprfields__.values ();
		let fields = [];
		for (let name of names) {{
		    fields.push (name + '=' + repr (self [name]));
		}}
		return  self.__name__ + '(' + ', '.join (fields) + ')'
	});},
	get __eq__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__eq__(list (otherFields));
	});},
	get __ne__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__ne__(list (otherFields));
	});},
	get __lt__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__lt__(list (otherFields));
	});},
	get __le__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__le__(list (otherFields));
	});},
	get __gt__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__gt__(list (otherFields));
	});},
	get __ge__ () {return __get__ (this, function (self, other) {
		let names = self.__comparefields__.values ();
		let selfFields = [];
		let otherFields = [];
		for (let name of names) {
		    selfFields.push (self [name]);
		    otherFields.push (other [name]);
		}
		return list (selfFields).__ge__(list (otherFields));
	});},
	nam: 'val',
	unit_price: 0.5,
	quantity_on_hand: 0,
	get compute () {return __get__ (this, function (self) {
		return self.unit_price * self.quantity_on_hand;
	});}
})
for (let aClass of InventoryItem.__bases__) {
	__mergefields__ (InventoryItem, aClass);
};
__mergefields__ (InventoryItem, {__reprfields__: new Set (['nam', 'unit_price', 'quantity_on_hand']), __comparefields__: new Set (['nam', 'unit_price', 'quantity_on_hand']), __initfields__: new Set (['nam', 'unit_price', 'quantity_on_hand'])});

//# sourceMappingURL=web.common.map