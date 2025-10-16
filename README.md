# PyObjectInterface

![Tests Badge](https://github.com/RobertJN64/PyObjectInterface/actions/workflows/tests.yml/badge.svg)
![Python Version Badge](https://img.shields.io/pypi/pyversions/PyObjectInterface)
![License Badge](https://img.shields.io/github/license/RobertJN64/PyObjectInterface)

Quickly control any python object through an async web interface.

`pip install PyObjectInterface`
```python
from PyObjectInterface.WebController import create_WebController
import flask

app = flask.Flask('Demo')
any_python_object = ...
create_WebController(any_python_object, 'any_python_object', app)
app.run()
```

Go to `http://127.0.0.1:5000/webcontroller`

## Example: Async Robot Control
![async_robot_control.png](async_robot_control.png)

The above interface was automatically created from:
```python
class DriveMotor:
    def __init__(self, pin):
        self.pin = pin
        self.speed = 0

    def forward(self): ...
    def stop(self): ...

class Robot:
    def __init__(self):
        self.left_motor = DriveMotor(1)
        self.right_motor = DriveMotor(2)

    def forward(self): ...
    def stop(self): ...
    def left(self): ...
    def right(self): ...
```

Look at [PyObjectInterface/examples/example.py](PyObjectInterface/examples/example.py) for more information.

## Advanced Usage and Settings

You can use PyObjectInterface without the WebController.

### create_WebController
 - `obj`: Any python object
 - `name: str`: Friendly name for object, generally the name of the variable that refers to the object
 - `flask_app`: return value of flask.Flask()
 - `recursion_depth = 5`: maximum layers of subobjects to include
 - `create_private_interface = True`: if `True` creates a `/webcontroller/private` page that includes private methods and attributes

### Modifying Attributes

By default, POI treats `NoneType, bool, int, float, str, list, dict, tuple, and set` as primitive types.
These show up in the attribute table instead of as recursive objects.

`numpy.ndarray`, `pandas.DataFrame`, and `pandas.Series` are also treated as primitives.

Note: numpy 2.0 arrays currently do not work with python's inspect library, 
and therefore must be treated as a primitive.
For Python >= 3.13 on windows, numpy >= 2.0 must be used.

If you would like to customize this behavior, you can modify
`PyObjectInterface.basic_attribute_types`

For example:
```python
from PyObjectInterface import basic_attribute_types

class My_Class_A: ...
class My_Class_B: ...
class My_Class_C: ...

basic_attribute_types[str(type(My_Class_A()))] = False
basic_attribute_types[str(type(My_Class_B()))] = True
```

`My_Class_A` will be treated as a primitive and only show up in the attributes table.
`My_Class_B` will also show up in attributes table, but it still appears in the subobjects section.
`My_Class_C` will only appear in the subobjects section.
