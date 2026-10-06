# Transfer learning: fine-tune a pretrained ResNet18 on CIFAR-10
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms
import torchvision.models as models
from torch.utils.data import DataLoader, Subset

# ---------- 0. Settings ----------
IMG_SIZE = 128                 # ResNet was trained on 224; 128 is faster on a laptop
N_TRAIN, N_TEST = 5000, 1000   # small subsets so it runs quickly
BATCH = 32
NUM_CLASSES = 10

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")
print("Using device:", device)

# ---------- 1. Data ----------
# ResNet expects the same normalization it was trained with (ImageNet mean/std)
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
testset = torchvision.datasets.CIFAR10(root='./data', train=False, download=True, transform=transform)

trainset = Subset(trainset, range(N_TRAIN))
testset = Subset(testset, range(N_TEST))

trainloader = DataLoader(trainset, batch_size=BATCH, shuffle=True)
testloader = DataLoader(testset, batch_size=BATCH, shuffle=False)

# ---------- 2. Load the pretrained model ----------
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# ---------- 3. Freeze the pretrained layers ----------
for param in model.parameters():
    param.requires_grad = False

# ---------- 4. Replace the last layer (new layers are trainable by default) ----------
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)   # 512 -> 10
model = model.to(device)

criterion = nn.CrossEntropyLoss()


# ---------- 5. Train / evaluate helpers ----------
def train(epochs, optimizer, backbone_trains):
    # frozen backbone -> keep it in eval mode so BatchNorm statistics stay fixed
    model.train() if backbone_trains else model.eval()
    for epoch in range(1, epochs + 1):
        running_loss = 0.0
        for images, labels in trainloader:
            images, labels = images.to(device), labels.to(device)

            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
        print(f"Epoch {epoch}, Loss: {running_loss / len(trainloader):.4f}")


def evaluate():
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    print(f"Accuracy: {100 * correct / total:.2f}%")


# ---------- 6. Phase 1: feature extraction (train only the new fc layer) ----------
print("\nPhase 1: training only the new final layer")
optimizer = optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)
train(epochs=3, optimizer=optimizer, backbone_trains=False)
evaluate()

# ---------- 7. Phase 2: fine-tuning (unfreeze everything, smaller learning rate) ----------
print("\nPhase 2: fine-tuning all layers")
for param in model.parameters():
    param.requires_grad = True

optimizer = optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
train(epochs=2, optimizer=optimizer, backbone_trains=True)
evaluate()
