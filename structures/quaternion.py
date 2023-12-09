#!/usr/bin/python3
"""
Quaternion package to test the algebra of quaternions.

Note: the definitions here use the same as ROS's tf package.
"""

import geometry_msgs.msg as gm
from tf.transformations import *
import sympy

class quaternion:
    """
    quaternion(q=[0, 0, 0, 0]: list[4]) -> q[0]*i + q[1]*j + q[2]*k + q[3]
        Default is the zero quaternion.
    """
    # Possible future signatures
    # quaternion() -> returns the zero quaternion -> 0
    # quaternion(real=s: number, imag=v: list[3]) -> v[0]*i + v[1]*j + v[2]*k + s
    # quaternion(q: Quaternion) -> returns a copy of the quaternion

    def __init__(self, q=[1, 0, 0, 0]):
        self.q = list(q)

    def __iter__(self):
        # i.e. for i in q: print(sympy.simplify(i))
        return iter(self.q)

    def __add__(self, other):
        return quaternion([s + t for s, t in zip(self, other)])

    def __mul__(self, other):
        q = quaternion()
        q.x = self[3]*other[0] + self[0]*other[3] + self[1]*other[2] - self[2]*other[1]
        q.y = self[3]*other[1] - self[0]*other[2] + self[1]*other[3] + self[2]*other[0]
        q.z = self[3]*other[2] + self[0]*other[1] - self[1]*other[0] + self[2]*other[3]
        q.w = self[3]*other[3] - self[0]*other[0] - self[1]*other[1] - self[2]*other[2]
        return q

    def __neg__(self):
        return Quaternion([-s for s in self.q])

    def __sub__(self, other):
        return quaternion([s - t for s, t in zip(self, other)])

    def __getitem__(self, index):
        return self.q[index]

    def __setitem__(self, index, value):
        self.q[index] = value

    def __str__(self):
        return str(self.q)

    def conjugate(self):
        """ Returns the quaternion conjugate. """
        q = quaternion()
        q.x = -self.x
        q.y = -self.y
        q.z = -self.z
        q.w = self.w
        return quaternion(q)

    def cross(self, other):
        """ Returns the pure quaternion cross product. """
        return (self.imag()*other.imag()).imag()

    def dot(self, other):
        """ Returns the pure quaternion dot product. """
        return (self.imag()*other.imag()).real()

    def imag(self):
        """ Returns the imaginary part of the quaternion. """
        q = quaternion()
        q.x = self.x
        q.y = self.y
        q.z = self.z
        q.w = 0
        return q

    def quadrature(self):
        """ Returns the square of the length. """
        return sum(s*s for s in self)

    def real(self):
        """ Returns the real part of the quaternion. """
        q = quaternion()
        q.w = self.w
        return q

    def rotate(self, other):
        """ Rotates (pure) quaternion by other. """
        return other*self*other.conjugate()

    @property
    def x(self):
        return self.q[0]

    @property
    def y(self):
        return self.q[1]

    @property
    def z(self):
        return self.q[2]

    @property
    def w(self):
        return self.q[3]

    @x.setter
    def x(self, val):
        self.q[0] = val

    @y.setter
    def y(self, val):
        self.q[1] = val

    @z.setter
    def z(self, val):
        self.q[2] = val

    @w.setter
    def w(self, val):
        self.q[3] = val

if __name__ == "__main__":
    qx, qy, qz, qw = sympy.symbols("q.x, q.y, q.z, q.w")
    vx, vy, vz = sympy.symbols("v.x, v.y, v.z")
    wx, wy, wz = sympy.symbols("w.x, w.y, w.z")
    q = quaternion([qx, qy, qz, qw])
    v = quaternion([vx, vy, vz, 0])
    w = quaternion([wx, wy, wz, 0])

    print("Rotation Matrix Derivation")
    rotated = v.rotate(q)
    for item in rotated:
        print(sympy.collect(sympy.expand(sympy.simplify(item)), (vx, vy, vz)))

    print("tf2 comparison (These should all be approx [0, 0, 0, 0])")
    for i in range(10):
        q1t = random_quaternion()
        q2t = random_quaternion()
        q1s = quaternion(q1t)
        q2s = quaternion(q2t)
        print(q1s*q2s - quaternion_multiply(q1t, q2t))

    print("Fictious forces")
    coriolis = w.cross(v.rotate(q)) # This isn't symplified
    for item in coriolis:
        print(sympy.collect(sympy.expand(sympy.simplify(item)), (wx, wy, wz)))
