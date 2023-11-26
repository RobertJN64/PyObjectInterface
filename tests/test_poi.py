from PyObjectInterface import PyObjectInterface

class Basic:
    def __init__(self):
        self.attr_1 = 2
        self.attr_2 = 2

    def method_1(self):
        pass

    def method_2(self, a, b=5):
        pass

def test_basic():
    basic = Basic()
    poi = PyObjectInterface(basic, 'Basic')
    assert 'attr_1' in poi.attribute_list
    assert 'attr_2' in poi.attribute_list
    assert 'method_1' in poi.method_dict
    assert 'method_2' in poi.method_dict

#TODO - 100% test coverage