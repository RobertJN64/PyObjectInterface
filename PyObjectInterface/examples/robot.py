class DriveMotor:
    def __init__(self, pin):
        self.pin = pin
        self.speed = 0

    def forward(self):
        self.speed = 50

    def stop(self):
        self.speed = 0

class Robot:
    def __init__(self):
        self.left_motor = DriveMotor(1)
        self.right_motor = DriveMotor(2)

    def forward(self):
        self.left_motor.forward()
        self.right_motor.forward()

    def stop(self):
        self.left_motor.stop()
        self.right_motor.stop()

    def left(self):
        self.left_motor.stop()
        self.right_motor.forward()

    def right(self):
        self.left_motor.forward()
        self.right_motor.stop()