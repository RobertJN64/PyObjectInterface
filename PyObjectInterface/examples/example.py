from PyObjectInterface.WebController import create_WebController
from robot import Robot
import flask

app = flask.Flask('Demo')
robot = Robot()
create_WebController(robot, 'robot', app)
app.run()