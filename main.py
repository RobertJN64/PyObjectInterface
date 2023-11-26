from PyObjectInterface.WebController import create_WebController
import flask

class Obj:
    def __init__(self):
        pass

    def return_value(self):
        return 'hello'

    def error_2(self):
        self.error()

    def error(self):
        raise UserWarning("HELP!")

app = flask.Flask(__name__)
obj = Obj()
create_WebController(obj, 'obj', app)
app.run()