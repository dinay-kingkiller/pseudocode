"""
motion (F_k): maps state (x_k-1) -> next_state (x_k)
observation (H_k): maps state (x_k) -> measurement (z_k)
control (B_k): maps input (u_k) -> state (x_k)
state_error (P_k)
noise_error (Q_k)
measurement_error (R_k)
innovation (y_k)
innovation_error (S_k)
gain (K_k)
current process assumes motion, observation, and control are static
"""
try:
	from numpy.linalg import inv as inverse
	from numpy import matrix, transpose, zeros
except ImportError:
    raise ImportError, "The numpy and scipy modules are required for this class (Kalman.py)"
class KalmanFilter:
	def __init__(self, motion, control, observation, initial_state = None, initial_measurement = None):
		self.motion = matrix(motion)
		self.control = matrix(control)
		self.observation = matrix(observation)
		if initial_state is not None:
			self.state = matrix(initial_state)
		elif initial_measurement is not None:
			self.state = self.observation * matrix(initial_measurement)
		else:
			raise IllegalArgumentException('either initial_state or initial_measurement must be defined') 
		state_dim = len(self.motion)
		measure_dim = len(self.observation)
		self.state_error = zeros(state_dim, state_dim)
		self.measurement_error = zeros(measure_dim, measure_dim)
	def predict(self, input):
		input = matrix(input)
		self.state = self.motion*self.state + self.control*input
		self.state_error = self.motion*self.state_error*transpose(self.motion) + self.noise_error
	def measure(self, measurement):
		measurement = matrix(measurement)
		innovation = measurement - self.observation*self.state
		innovation_error = self.observation*self.covariance*transpose(self.observation) + self.measurement_error
		gain = self.covariance * transpose(self.observation) * inverse(innovation_error)
		self.state = self.state + gain*innovation
		self.state_error = self.state_error - gain*self.observation_error*self.state_error
