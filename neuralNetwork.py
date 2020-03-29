from matrix import Matrix 
import random
import math

def sigmoid(x):
	return 1/(1+math.exp(-x))

def Dsigmoid(y):
	#return sigmoid(x) * (1- sigmoid(x))
	return y * (1-y)

class NeuralNetwork:
	def __init__(self,a):
		if isinstance(a, NeuralNetwork):
			self.input_nodes = a.input_nodes
			self.hidden_nodes = []
			for i in range(len(a.hidden_nodes)):
				self.hidden_nodes.append(a.hidden_nodes[i])
			self.output_nodes = a.output_nodes
			
			self.weights_ih = a.weights_ih.copy()
			self.weights_hh = []
			for i in range(len(a.weights_hh)):
				self.weights_hh.append(a.weights_hh[i].copy())
			self.weights_ho = a.weights_ho.copy()

			self.bias_h = []
			for i in range(len(a.bias_h)):
				self.bias_h.append(a.bias_h[i].copy())
			self.bias_o = a.bias_o.copy()
		else:
			self.input_nodes = a[0]
			self.hidden_nodes = []
			for i in range(1,len(a)-1):
				self.hidden_nodes.append(a[i])
			self.output_nodes = a[len(a)-1]

			self.weights_ih = Matrix(self.hidden_nodes[0], self.input_nodes)
			self.weights_hh = [] * (len(a)-3)
			if len(a)>=3:
				for i in range(0,len(a)-3):
					self.weights_hh.append(Matrix(self.hidden_nodes[i+1],self.hidden_nodes[i]))
					self.weights_hh[i].randomize() 
			self.weights_ho = Matrix(self.output_nodes, self.hidden_nodes[len(self.hidden_nodes)-1])
			self.weights_ih.randomize()
			self.weights_ho.randomize()
			self.bias_h = []

			for i in range(len(a)-2):
				self.bias_h.append(Matrix(self.hidden_nodes[i], 1))
				self.bias_h[i].randomize()

			self.bias_o = Matrix(self.output_nodes, 1)
			self.bias_o.randomize()

			self.learning_rate = 0.1

	def feedforward(self,input_array):
		#Generating Hidden outputs
		inputs = Matrix().fromArray(input_array)

		hidden = Matrix().multiply(self.weights_ih, inputs)
		hidden.add(self.bias_h[0])
		#activation Function
		hidden.map(sigmoid)
		internal=None
		for i in range(len(self.weights_hh)):
			internal=Matrix().multiply(self.weights_hh[i],hidden)
			internal.add(self.bias_h[i+1])
			internal.map(sigmoid)
			hidden=internal

		#Generating outputs
		output = Matrix().multiply(self.weights_ho, hidden)
		output.add(self.bias_o)
		output.map(sigmoid)

		return output.toArray()

	def train(self,inp, targets):
		#Generating Hidden outputs
		inputs = Matrix().fromArray(inp)
		hidden = Matrix().multiply(self.weights_ih, inputs)
		hidden.add(self.bias_h[0])
		#activation Function
		hidden.map(sigmoid)
		
		hidden_output = []
		hidden_output.append(hidden)

		for i in range(len(self.weights_hh)):
			internal=Matrix().multiply(self.weights_hh[i],hidden)
			internal.add(self.bias_h[i+1])
			internal.map(sigmoid)
			hidden=internal
			hidden_output.append(hidden)
		
		index = len(hidden_output)-1

		#Generating outputs
		outputs = Matrix().multiply(self.weights_ho, hidden_output[index])
		outputs.add(self.bias_o)
		outputs.map(sigmoid)

		#Convert array to matrix
		targets = Matrix().fromArray(targets)
		#Calculate output error
		output_errors = Matrix().subtract(targets,outputs)
		#Calculate Gradient
		gradients = Matrix().map(outputs, Dsigmoid)
		gradients.multiply(output_errors)
		gradients.multiply(self.learning_rate)

		#Calculate deltas
		hidden_T = Matrix().transpose(hidden_output[index])
		weights_ho_deltas = Matrix().multiply(gradients, hidden_T)
		
		self.weights_ho.add(weights_ho_deltas)
		self.bias_o.add(gradients)

		who_t = Matrix().transpose(self.weights_ho)
		index -= 1
		hidden_errors = Matrix().multiply(who_t, output_errors)
		
		for i in range(len(self.weights_hh)-1,-1,-1):
			#Calculate Gradient
			hidden_gradients = Matrix().map(hidden_output[index+1], Dsigmoid)
			hidden_gradients.multiply(hidden_errors)
			hidden_gradients.multiply(self.learning_rate)

			#Calculate deltas
			inner_hidden_T = Matrix().transpose(hidden_output[index])
			weights_hh_deltas = Matrix().multiply(hidden_gradients, inner_hidden_T)
		
			self.weights_hh[i].add(weights_hh_deltas)
			self.bias_h[i+1].add(hidden_gradients)

			whh_t = Matrix().transpose(self.weights_hh[i])
			index -= 1
			new_errors = Matrix().multiply(whh_t, hidden_errors)
			hidden_errors = new_errors

		#Hidden Gradients
		hidden_gradient = Matrix().map(hidden_output[0], Dsigmoid)
		hidden_gradient.multiply(hidden_errors)
		hidden_gradient.multiply(self.learning_rate)

		#Calculate deltas
		inputs_T = Matrix().transpose(inputs)
		weights_ih_deltas = Matrix().multiply(hidden_gradient, inputs_T)

		self.weights_ih.add(weights_ih_deltas)
		self.bias_h[0].add(hidden_gradient)

	def copy(self):
		return NeuralNetwork(self)

	def mutate(self,rate):

		def mutate(val):
			if random.random() < rate:
				return val + random.gauss(0, 0.1)
			else:
				return val

		self.weights_ih.map(mutate)
		for i in range(len(self.weights_hh)):
				self.weights_hh[i].map(mutate)
		self.weights_ho.map(mutate)
		
		for i in range(len(self.bias_h)):
				self.bias_h[i].map(mutate)
		self.bias_o.map(mutate)
	
	def save(self,name):
		savefile = open(name+'.nn', 'wb')
		import pickle
		pickle.dump(self,savefile)
		savefile.close()
		return True
	
	def load(self, name):
		try:
			savefile = open(name+'.nn', 'rb')
			import pickle
			nn = pickle.load(savefile)
			savefile.close()
			return nn
		except IOError:
			print('File not found, need to train...')
			return None

		