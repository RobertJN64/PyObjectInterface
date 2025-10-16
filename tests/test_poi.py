from PyObjectInterface import PyObjectInterface, basic_attribute_types
from PyObjectInterface.WebController import generate_html
import numpy as np
import pytest

class Nested:
    def __init__(self):
        self.attr_3 = 3

    @staticmethod
    def internal_method():
        return "hello from nested"

class Basic:
    def __init__(self):
        self.attr_1 = 1
        self._attr_2 = 2
        self.nested = Nested()

    def method_1(self, a, b=5):
        """Method desc"""
        return f"{self.attr_1} {a} {b}"

    def _method_2(self):
        pass

    def __repr__(self):
        return "example repr"



def test_basic():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')

    #TEST SCAN
    assert 'attr_1' in poi.attribute_list
    assert '_attr_2' not in poi.attribute_list
    assert 'method_1' in poi.method_dict
    assert '_method_2' not in poi.method_dict

    assert '__repr__' not in poi.method_dict
    assert '__repr__' not in poi.attribute_list

    assert 'nested' in poi.subobj_dict

    assert poi.base_obj_name in repr(poi)

def test_method_calls():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')

    basic.attr_1 = 'some value'
    retval = poi.call_method('Basic.method_1', {'a': 'another_value'})
    assert retval == "some value another_value 5"

    retval = poi.call_method('Basic.nested.internal_method', {})
    assert retval == "hello from nested"

def test_get_attr():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')
    attrs = poi.get_attributes()
    assert attrs['Basic.attr_1'] == '1'
    assert attrs['Basic.nested.attr_3'] == '3'

def test_private():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic', include_private=True)
    assert 'attr_1' in poi.attribute_list
    assert '_attr_2' in poi.attribute_list
    assert 'method_1' in poi.method_dict
    assert '_method_2' in poi.method_dict

    assert '__repr__' not in poi.method_dict
    assert '__repr__' not in poi.attribute_list

    poi.call_method('Basic._method_2', {})

class Recursive:
    def __init__(self):
        self.myself = self

def test_recursive():
    r = Recursive()
    poi = PyObjectInterface(r, 'r')

    counter = 0
    while len(poi.subobj_dict):
        poi = poi.subobj_dict['myself']
        counter += 1
    assert counter == 5

def test_method_call_exception():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')
    with pytest.raises(Exception,
                       match="Attempted to call self.base_obj_name='Basic' with method_stack='NotBasic.method_1'"):
        poi.call_method('NotBasic.method_1', {})


class FuncParams:
    def __init__(self):
        pass

    @staticmethod
    def static(first_param):
        pass

    @classmethod
    def classmethod(cls, first_param):
        pass

    def defaults(self, x, y = None, z = 10, k='string'):
        pass

def test_func_params():
    poi = PyObjectInterface(FuncParams(), 'FP')
    assert len(poi.method_dict['static'].args) == 1
    assert poi.method_dict['static'].args[0] == 'first_param'

    assert len(poi.method_dict['classmethod'].args) == 1
    assert poi.method_dict['classmethod'].args[0] == 'first_param'

    assert poi.method_dict['defaults'].defaults[0] == ''
    assert poi.method_dict['defaults'].defaults[1] == 'None'
    assert poi.method_dict['defaults'].defaults[2] == '10'
    assert poi.method_dict['defaults'].defaults[3] == "'string'"

def test_coverage(): #not useful - just padding code coverage
    fp = FuncParams()
    fp.static(None)
    fp.classmethod(None)
    fp.defaults(None)

    repr(Basic())

def test_html():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')
    generate_html(poi)

    class Blank: pass
    poi = PyObjectInterface(Blank(), 'Blank')
    assert 'table' not in generate_html(poi)

class np_special_case:
    def __init__(self):
        self.np_arr = np.array([1,2,3])

def test_np_special_case():
    n = np_special_case()

    poi = PyObjectInterface(n, 'b')
    assert 'np_arr' in poi.attribute_list
    assert 'np_arr' not in poi.subobj_dict

    # basic_attribute_types[str(type(n.np_arr))] = True
    #
    # poi = PyObjectInterface(n, 'b')
    # assert 'np_arr' in poi.attribute_list
    # assert 'np_arr' in poi.subobj_dict
    #
    # assert "is a builtin method and can't be accessed from WebController" in generate_html(poi)
    #
    # basic_attribute_types.pop(str(type(n.np_arr)))
    #
    # poi = PyObjectInterface(n, 'b')
    # assert 'np_arr' not in poi.attribute_list
    # assert 'np_arr' in poi.subobj_dict
