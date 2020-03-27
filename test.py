from neuralNetwork import NeuralNetwork
import random

def XOR(a,b):
    if a==b:
        return 0
    else:
        return 1

nn = NeuralNetwork([24,18,18,4])

for i in range(150000):
    inp = []
    for j in range(24): 
        inp.append(random.randint(0,1))
    op = [XOR(inp[0],inp[1]), XOR(inp[5],inp[8]), XOR(inp[4],inp[18]), XOR(inp[20],inp[23])]
    nn.train(inp,op)

nn.save('savedBrain')
