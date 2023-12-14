from typing_extensions import Self
import inspect

# {type: examine_recursively}
basic_attribute_types = {
    str(type(None)): False,  #NoneType
    str(type(True)): False,  #bool
    str(type(1)): False,     #int
    str(type(1.0)): False,   #float
    str(type('1')): False,   #str
    str(type([1])): False,   #list
    str(type({1:1})): False, #dict
    str(type((1,1))): False, #tuple
    str(type({1})): False,   #set
    "<class 'numpy.ndarray'>": False,
    "<class 'pandas.core.frame.DataFrame'>": False,
    "<class 'pandas.core.series.Series'>": False
}

class FunctionDesc:
    def __init__(self, func):
        self.func = func
        self.desc = func.__doc__
        self.builtin_err = False

        try:
            params = inspect.signature(func).parameters
            self.args = list(params.keys())
        except ValueError:
            params = []
            self.args = []
            self.builtin_err = True

        self.defaults = []
        for arg in self.args:
            if params[arg].default is params[arg].empty:
                self.defaults.append("")
            else:
                self.defaults.append(repr(params[arg].default))

    def __repr__(self):
        return f"{self.args=} {self.defaults=}"

class PyObjectInterface:
    def __init__(self, obj: object, base_obj_name: str, include_private: bool = False, recursion_depth: int = 5):
        """
        Create a PyObjectInterface
        :param obj: Any python object
        :param base_obj_name: Name of the refrence to the object
        :param include_private: Include private methods and attributes
        :param recursion_depth: How many layers of nested objects to include, 0 = no recursion
        """

        self.obj = obj
        self.base_obj_name = base_obj_name

        self.method_dict: dict[str, FunctionDesc] = {} #dictionary of function names and FunctionDescs
        self.attribute_list: list[str] = [] #list of attribute_names
        self.subobj_dict: dict[str, Self] = {} #dictionary of object names and PyObjectInterfaces

        if include_private:
            all_attrs = [x for x in inspect.getmembers(obj) if x[0][0:2] != '__'] #ignore dunder methods
        else:
            all_attrs = [x for x in inspect.getmembers(obj) if x[0][0:1] != '_'] #ignore private

        for (attr_name, instance) in all_attrs:
            if str(type(instance)) in basic_attribute_types:
                self.attribute_list.append(attr_name)
                if not basic_attribute_types[str(type(instance))]:
                    continue #skip the rest of the checks, we don't want to examine this item recursively

            if hasattr(instance, '__call__'):
                self.method_dict[attr_name] = FunctionDesc(instance)

            elif recursion_depth > 0: #stop adding subobjects at recursion depth 0
                # using .__class__ allows superclassing
                # noinspection PyTypeChecker
                self.subobj_dict[attr_name] = self.__class__(instance, self.base_obj_name + '.' + attr_name,
                                                             include_private, recursion_depth-1)

    def get_attributes(self):
        """
        Returns a dictionary of the form: {base_obj_name.attribute_name: attribute_value}
        """
        retval = {}
        for attribute_name in self.attribute_list:
            retval[self.base_obj_name + '.' + attribute_name] = str(getattr(self.obj, attribute_name))
        for obj in self.subobj_dict.values():
            retval.update(obj.get_attributes())
        return retval

    def call_method(self, method_stack: str, kwargs: dict):
        """
        Call a method of obj or a subobj using base_obj_name.subobj_name.method(**kwargs)
        """
        if not method_stack.startswith(self.base_obj_name + '.'):
            raise Exception(f"Attempted to call {self.base_obj_name=} with {method_stack=}")

        method_name = method_stack[len(self.base_obj_name + '.'):] #rm prefix
        if '.' in method_name:
            obj_name = method_name.split('.')[0]
            return self.subobj_dict[obj_name].call_method(method_stack, kwargs)
        else:
            return self.method_dict[method_name].func(**kwargs)

    def __repr__(self):
        return (f"PyObjectInterface of {self.base_obj_name} with:"
                f"\nmethods:\n{self.method_dict}" +
                f"\nattributes:\n{self.attribute_list}"
                f"\nsubobjects: {list(self.subobj_dict.keys())}")


