import random

class Matrix:
	def __init__(self,rows=0,cols=0):
		self.cols=cols
		self.rows=rows
		self.data=[[0 for i in range(cols)] for j in range(rows)]

	def fromArray(self,arr):
		m = Matrix(len(arr),1)
		for a in range(len(arr)):
			m.data[a][0]= arr[a]
		return m
	
	def toArray(self):
		arr=[]
		for i in range(self.rows):
			for j in range(self.cols):
				arr.append(self.data[i][j])
		return arr

	def transpose(self,m):
		result=Matrix(m.cols,m.rows)
		for i in range(m.rows):
			for j in range(m.cols):
				result.data[j][i]=m.data[i][j]
		return result
	
	def subtract(self, m1, m2): 
		result = Matrix(m1.rows, m1.cols)
		for i in range (m1.rows):
			for j in range(m2.cols):
				result.data[i][j] = m1.data[i][j] - m2.data[i][j]
		return result

	def randomize(self): 
		for i in range(self.rows): 
			for j in range(self.cols):
				self.data[i][j] = random.random() * 2 - 1

	def multiply(self,*args): 
		if len(args) is 1:
			if (isinstance(args[0],Matrix)):
				#hadamard product
				for i in range(self.rows): 
					for j in range(self.cols):  
						self.data[i][j] *= args[0].data[i][j]
			else: 
				for i in range(self.rows):
					for j in range(self.cols):
						self.data[i][j] *= args[0]
		else:
			# print("CALLED")
			# print(args[0].cols, args[1].rows)
			if (args[0].cols != args[1].rows):
				return None
				#print("Columns Rows Are not same!!") change 2
			result = Matrix(args[0].rows, args[1].cols)
			for i in range(result.rows):
				for j in range(result.cols):
					sum = 0
					for k in range(args[0].cols):
						sum += args[0].data[i][k] * args[1].data[k][j]
					result.data[i][j] = sum
			return result
		
	def add(self,n): 
		if (isinstance(n,Matrix)):
			#hadamard product
			for i in range(self.rows): 
				for j in range(self.cols):  
					self.data[i][j] += n.data[i][j]
		else:
			for i in range(self.rows):
				for j in range(self.cols):
					self.data[i][j] += n

	def print(self): 
		print("rows",self.rows,"cols",self.cols)
		for i in range(self.rows):
				for j in range(self.cols):
					print((str)(self.data[i][j])+" ",end="\t")
				print()
	
	def map(self,*args):
		if len(args) is 1:
			for i in range(self.rows): 
				for j in range(self.cols): 
					val = self.data[i][j]
					self.data[i][j] = args[0](val)
		else:
			result = Matrix(args[0].rows, args[0].cols)
			for i in range(args[0].rows):
				for j in range(args[0].cols): 
					val = args[0].data[i][j]
					result.data[i][j] = args[1](val)
			return result

	def copy(self):
		result = Matrix(self.rows, self.cols)
		for i in range(result.rows): 
			for j in range(result.cols): 
				result.data[i][j] = self.data[i][j]
		return result