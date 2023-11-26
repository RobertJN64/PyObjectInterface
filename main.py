# PyObjectInterface import PyObjectInterface
from PyObjectInterface.WebController import create_WebController
import flask

class A:
    def __init__(self):
        self.x = None
        self.y = 5
        self._t = 7

    def example(self, z=None, k=10):
        pass

    def example_2(self, z=None, k=10):
        """
        Some example func desc
        :param z: some info
        :param k: x
        """

a = A()
a.b = A()
app = flask.Flask(__name__)
create_WebController(a, 'a', app)
app.run()