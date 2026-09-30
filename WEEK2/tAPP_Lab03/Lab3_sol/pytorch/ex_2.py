import torch
import torch.nn as nn

class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()

        self.fc1 = nn.Linear(784, 128) # Input 
        self.fc2 = nn.Linear(128, 64) # Hidden Layer
        self.fc3 = nn.Linear(64, 10) # Output Layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.softmax(self.fc3(x), dim=1)
        return x

model = SimpleNN()
print(model)