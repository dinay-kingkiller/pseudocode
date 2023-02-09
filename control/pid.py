# pid.py
"""
A PID is one of the most basic controllers for feedback control. Given an
error signal, the controller will give you a signal that lets you reduce
the error in the next update.
Very generally the parameters can be described as follows:
    P = proportional term: reduces the offset from the goal
        a pure propotional controller could work, but only if the
        process is constant
    I = integral term: reduces drift from the goal.
        Increasing could lead to overshoot, decreasing the time to reach
        the goal
    D = differential term: reduces noise in the error signal, decreasing
        the time to reach the goal
# Possible Example, given outside information about the process and
# measurement.
controller = PID(P, I, D)
while:
    error = goal - measurement()
    update = controller.update(error)
    process(update)
"""


class pid:
    def __init__(self, P, I=0, D=0):
        self.P = P
        self.I = I
        self.D = D
        self.sumError = 0
        self.lastError = 0

    def update(self, error):
        self.sumError += error
        diffError = error - self.lastError
        self.lastError = error
        return self.P*error + self.I*self.sumError + self.D*diffError
