#mcl.py
from __future__ import division
try:
    from numpy import zeros, rank, shape, prod, sum, matrix
except ImportError:
    raise ImportError,"The numpy and scipy modules are required"
class mcl:
    """
    This class implements 2 Dimensional Monte-Carlo Localization
    """
    NUM_DIM=2
    def __init__(self,world,init_pos=None,init_prob=1,move_prob=1,meas_prob=1):
        if rank(world)==1:
            world=[world]
        if rank(world)!=self.NUM_DIM:
            raise TypeError, "world has too many dimensions"
        self.move_prob=move_prob
        self.stay_prob=1-move_prob
        self.meas_prob=meas_prob
        self.miss_prob=1-meas_prob
        self.world=world
        self.dim=shape(world)
        if init_pos==None:
            val=1/prod(self.dim)
            self.belief=[[val for i in range(self.dim[1])]\
            for i in range(self.dim[0])]
        else:
            self.belief=zeros(self.dim)
            self.belief[init_pos[0]][init_pos[1]]=1/init_prob
            self.belief=self.belief/norm(self.belief)
    def move(self,motion):
        if len(motion)==self.NUM_DIM:
            aux=zeros(self.dim)
            for i in range(self.dim[0]):
                for j in range(self.dim[1]):
                    aux_move=self.move_prob*self.belief[(i-motion[0])%self.dim[0]]\
                    [(j-motion[1])%self.dim[1]]
                    aux_stay=self.stay_prob*self.belief[i][j]
                    aux[i][j]=aux_move+aux_stay
            self.belief=aux
        else:
            raise ValueError, "Motion vector is not 2D"
    def sense(self,measurement):
        for i in range(self.dim[0]):
            for j in range(self.dim[1]):
                hit=self.world[i][j]==measurement
                self.belief[i][j]*=self.meas_prob*hit+self.miss_prob*(1-hit)
        self.belief=self.belief/sum(self.belief)
