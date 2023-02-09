# particle.py
"""
particle filter for a robot
robot class must have a constructor that provides no inputs and creates a robot
with a random state. It must have a move function that simulates motion and a
position attribute that is a list of its x and y position
"""
from __future__ import division
from random import random
from math import pi


class particle:
    def __init__(self, robot, particleCount, landmarks, move_noise=.5, sense_noise=.5):
        """
            @param robot: robot class
            @param particleCount: number of particles for simulation
            @param landmarks: the position of the landmarks on the map
            @param move_noise:
            @param sense_noise:
        """
        self.particles = [robot() for i in range(particleCount)]
        self.landmarks = landmarks
        self.num_dim = len(landmarks[0])

    def update(self, motion, measurement):
        """
        iterates through the particles, choosing the best that fit the robot
            @param motion: the vector of motion the robot uses to use its move method
            @param measurement: the measured relative position between the robot and the landmarks
        """
        w = [0] * len(self.particles)
        for i, particle in enumerate(self.particles):
            particle.move(motion)
            prob = 1
            for j in range(len(landmarks))):
                sum2=0  # sum of squares
                for k in range(self.num_dim):
                    sum2 += (particle.pos[k] - landmarks[j][k])**2
                distance=sqrt(sum2)
                prob *= Gaussian(distance, self.sense_noise, measurement[i])
            w[i]=prob
        index=int(random() * len(self.particles))
        beta=0.0
        newP=copy(p)
        for i in range(len(self.particles)):
            beta += 2 * max(w) * random()
            while beta > w[index]:
                beta -= w[index]
                index=(index+1) % self.num_particles
            newP[i]=p[index]
    def Gaussian(mean, dev, x):
        return exp(-(mean-x)**2 / (2*dev**2)) / sqrt(2*pi*(mean**2))
