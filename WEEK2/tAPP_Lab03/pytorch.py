import torch
import torch.nn as nn
import torch.nn.functional as F
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt

x = torch.linspace(-10, 10, 100)

y = torch.sigmoid(x)

plt.plot(x.numpy(), y.numpy(), color='purple')
plt.xlabel('Input')
plt.ylabel('Output')
plt.title('Logistic Activation Function')
plt.show()

y = torch.tanh(x)

plt.plot(x.numpy(), y.numpy(), color='blue')
plt.xlabel('Input')
plt.ylabel('Output')
plt.title('Hyperbolic Tangent')
plt.show()


y = torch.relu(x)

plt.plot(x.numpy(), y.numpy(), color='green')
plt.xlabel('Input')
plt.ylabel('Output')
plt.title('ReLu Activation Function')
plt.show()

# Cros Entropy Loss -> Classification
# MSE -> Regression

# Optimizer :
# Updates Neural Network Weights based on Gradient loss 
# functions w.r.t weights. The goal is to minimize the loss function
# by iteratively adjusting the weights
# Stochastic GD, Adam(Adaptive Moment Optimization)

# implement the training loop:
# nn learns from data. 
# Clear previous gradients optimizer.zero_grad()
# forward pass: outputs = model(inputs)
# compute loss: loss = criterion(outputs, targets)
# backpropagation: loss.backward()
# Update weights: optimizer.step()

# class SimpleNN(nn.Module):
#     def __init__(self):
#         super(SimpleNN, self).__init__()
        
#         # Define Layers
#         self.fc1 = nn.Linear(784, 128) # input: 784, output: 128
#         self.fc2 = nn.Linear(128, 64) # input: 128, output: 64
#         self.fc3 = nn.Linear(64, 10) # input: 64, output: 10

#     def forward(self):
#         x = F.relu(self.fc1(x))

#         x = F.relu(self.fc2(x))

#         x = F.log_softmax(self.fc3(x), dim=1)

#         x = F.log_softmax(self.fc3(x), dim=1)

#         return x

# model = SimpleNN()

# print(model)