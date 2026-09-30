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

# Training the neural Network
import torch
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
# pyrefly: ignore [missing-import]
from torchvision import datasets, transforms


# Load MNIST dataset
transform = transforms.Compose([transforms.ToTensor()])
trainset = datasets.MNIST(root='./data', train=True, download=True, transform=transform)
trainloader = torch.utils.data.DataLoader(trainset, batch_size=32, shuffle=True)

# Define loss function and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01)

# Training Loop
for epoch in range(1, 6):
    running_loss = 0.0
    for images, labels in trainloader:
        images = images.view(images.shape[0], -1)
        optimizer.zero_grad()

        outputs = model(images)

        loss = criterion(outputs, labels)

        loss.backward()
        optimizer.step()

        running_loss += loss.item()
    print(f"Epoch {epoch}, Loss: {running_loss / len(trainloader)}")

print("Training Complete!")
