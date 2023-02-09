# gslam.py
try:
    from numpy import matrix, zeros, rank
    from scipy.linalg import solve, LinAlgError
except ImportError:
    raise ImportError, "The numpy and scipy modules are required"


class gslam:
    """
    GSLAM stands for graphical simultaneous localization and mapping
    it is a SLAM algorithm using a set of matrices to keep track of
    constraints derived    from movements and measurements
    """

    def __init__(self, init_pos, init_meas,
                 init_weight=1, move_weight=1, meas_weight=1):
        """
        sets up properties for the algorithm
        sets initial position and takes measurements there
        """
        # allows for a variety of formatted input
        while rank(init_pos) < 1:
            init_pos = [init_pos]
        while rank(init_meas) < 1:
            init_meas = [init_meas]
        if rank(init_meas) == 1:
            for i in range(len(init_meas)):
                if init_meas[i] != None:
                    init_meas[i] = [init_meas[i]]
        # set up properties for the algorithm
        self.num_dim = len(init_pos)
        self.num_landmarks = len(init_meas)
        self.matrix_dim = self.num_dim+self.num_landmarks
        self.omega = zeros([self.matrix_dim, self.matrix_dim])
        self.xi = zeros([self.matrix_dim, 1])
        self.init_weight = init_weight
        self.move_weight = move_weight
        self.meas_weight = meas_weight
        # sets initial position
        self.setPosition(init_pos)
        # takes measurements at initial position
        self.measure(init_meas)

    def update(self, move, meas=[[]]):
        """
        move the robot then take a measurement
        """
        self.move(move)
        self.measurement(move)

    def setPosition(self, pos):
        """
        adds a position constraint
        """
        for i in range(self.num_dim):
            self.omega[i][i] += self.init_weight
            self.xi[i][0] += pos[i]

    def measure(self, meas):
        """
        adds measurement constraints for each measurement of 
        the landmarks from the robot
        """
        while (rank(meas) < 1):
            meas = [meas]
        num_landmarks = len(meas)
        if rank(meas) == 1:
            for i in range(num_landmarks):
                if meas[i] != None and rank(meas[i]) == 0:
                    meas[i] = [meas[i]]
        while num_landmarks > self.num_landmarks:
            self.addLandmark()
        # measuring constraints
        for i in range(num_landmarks):
            if meas[i] != None:
                for j in range(self.num_dim):
                    self.omega[j][j] += self.meas_weight
                    self.omega[j][self.num_dim+i] -= self.meas_weight
                    self.omega[self.num_dim+i][j] -= self.meas_weight
                    self.omega[self.num_dim +
                               i][self.num_dim+i] += self.meas_weight
                    self.xi[j][0] -= self.meas_weight*meas[i][j]
                    self.xi[self.num_dim+i][0] += self.meas_weight*meas[i][j]

    def move(self, move):
        if rank(move) == 0:
            move = [move]
        if len(move) != self.num_dim:
            raise ValueError, "move must have same dimensions as it started"
        # copy the old position data
        A = zeros([self.num_dim, self.matrix_dim])
        B = matrix(zeros([self.num_dim, self.num_dim]))
        C = zeros([self.num_dim, 1])
        for i in range(self.num_dim):
            for j in range(self.num_dim):
                B[i][j] = self.omega[i][j]
            for j in range(self.num_landmarks):
                A[i][j+self.num_dim] = self.omega[i][j+self.num_dim]
            C[i][0] = self.xi[i][0]
        # clear room in omega and xi for new position
        for i in range(self.num_dim):
            for j in range(self.num_dim):
                self.omega[i][j] = 0
            for j in range(self.num_landmarks):
                self.omega[i][j+self.num_dim] = 0
                self.omega[j+self.num_dim][i] = 0
            self.xi[i][0] = 0
        # add movement constraints
        for i in range(self.num_dim):
            B[i][i] += self.move_weight
            A[i][i] -= self.move_weight
            self.omega[i][i] += self.move_weight
            C[i][0] -= self.move_weight*move[i]
            self.xi[i][0] += self.move_weight*move[i]
        # adjust omega and xi from previous position
        temp = A.T*B.I
        self.omega -= temp*A
        self.xi -= temp*C

    def getMu(self):
        """
        get function for matrix mu
        omega*mu=xi
        """
        try:
            return solve(self.omega, self.xi)
        except LinAlgError:
            if self.omega[self.matrix_dim-1][self.matrix_dim-1] == 0:
                self.removeLandmark()
                return self.mu
            else:
                raise LinAlgError, "One of the landmarks is undefined"
    mu = property(getMu)

    def getPos(self):
        """
        get function for the current position of the robot
        can fail if certain landmarks aren't defined
        """
        return self.mu[0:self.num_dim][0]
    pos = property(getPos)

    def getLandmarks(self):
        """
        get function for the position of the landmarks
        """
        return self.mu[self.num_dim+1:]
    landmarks = property(getLandmarks)

    def addLandmark(self):
        """
        add a row/column to omega and xi to allow for a new landmark
        """
        newDim = self.matrix_dim+1
        newOmega = zeros([newDim, newDim])
        newXi = zeros([newDim, 1])
        for i in range(self.matrix_dim):
            newXi[i][0] = self.xi[i][0]
            for j in range(self.matrix_dim):
                newOmega[i][j] = self.omega[i][j]
        self.num_landmarks += 1
        self.matrix_dim = newDim
        self.omega = newOmega
        self.xi = newXi

    def removeLandmark(self):
        """
        remove last landmark from omega and xi
        """
        newDim = self.matrix_dim-1
        newOmega = zeros([newDim, newDim])
        newXi = zeros([newDim, 1])
        for i in range(newDim):
            newXi[i][0] = self.xi[i][0]
            for j in range(newDim):
                newOmega[i][j] = self.omega[i][j]
        self.num_landmarks -= 1
        self.matrix_dim = newDim
        self.omega = newOmega
        self.xi = newXi
