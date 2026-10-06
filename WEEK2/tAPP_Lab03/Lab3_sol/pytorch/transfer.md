# Transfer Learning with ResNet18 (study guide for `transfer.py`)

How to use this guide:
1. Read Parts 1-3 once.
2. Read each block of Part 4 and **try the recall question before opening the answer**.
3. Do the rewrite exercises in Part 6 with `transfer.py` closed.

---

## Part 1. The idea in plain words

**Training from scratch (Task 1):** the network starts knowing nothing. It must first learn what edges, corners, textures and fur look like, *and then* what a cat is.

**Transfer learning:** someone already trained ResNet on ImageNet (1.2 million photos, 1000 classes). Its early layers already know edges, colours, textures and shapes. These skills are general and work on almost any photo. Only the **last layer** is specific to ImageNet, because it turns features into 1000 ImageNet labels.

So we:
- **keep** the pretrained feature layers,
- **replace** the last layer with a new one for *our* classes (10 for CIFAR-10),
- **train** it.

```
ResNet18 (pretrained)
[ early layers ] -> [ middle layers ] -> [ late layers ] -> [ fc: 512 -> 1000 ]
  edges, colours      shapes, textures     object parts       ImageNet labels
  \_______________ KEEP these _______________/                 \_ REPLACE: 512 -> 10
```

Analogy: hiring an experienced photographer and teaching them only your 10 new labels, instead of teaching a baby to see.

### Two ways to train it

| | Feature extraction | Fine-tuning |
|---|---|---|
| Pretrained layers | **frozen** (never change) | **unfrozen** (change a little) |
| New last layer | trained | trained |
| Speed | fast | slower |
| Learning rate | normal (0.001) | small (0.0001) |
| Risk | may underfit | may "forget" good features if the learning rate is too big |

`transfer.py` does both: **Phase 1** is feature extraction, then **Phase 2** is fine-tuning.

---

## Part 2. The 8 steps (memorise this list)

1. **Data**: resize to what ResNet expects and normalize with the **ImageNet** mean/std.
2. **Load** the pretrained model.
3. **Freeze** all its parameters.
4. **Replace** `model.fc` with a new `Linear(512, num_classes)`.
5. **Optimizer** over *only* the parameters that should train.
6. **Train** with the usual loop (zero, forward, loss, backward, step).
7. **Evaluate** on the test set.
8. **Fine-tune**: unfreeze, use a smaller learning rate, train a bit more, evaluate again.

Steps 6 and 7 are the loops you already know from Task 1. The new ideas are steps 1, 3, 4, 5 and 8.

---

## Part 3. What you need to know about ResNet18

- It is a CNN with **18 layers** that have weights.
- Print it with `print(model)`. The **last line** is `(fc): Linear(in_features=512, out_features=1000)`.
- So the final layer takes **512 numbers** (features for one image) and gives **1000 scores**.
- Shape trace for one batch (input size 128, batch `B`):

```
[B, 3, 128, 128]  input
conv1 (stride 2)  -> [B,  64, 64, 64]
maxpool           -> [B,  64, 32, 32]
layer1            -> [B,  64, 32, 32]
layer2            -> [B, 128, 16, 16]
layer3            -> [B, 256,  8,  8]
layer4            -> [B, 512,  4,  4]
avgpool           -> [B, 512,  1,  1]   (averages each 4x4 map to 1 number)
flatten           -> [B, 512]
fc (NEW)          -> [B,  10]
```

Key point: `avgpool` squeezes **any** image size down to 1x1. That is why the final layer is always 512 inputs, and why you could feed 64, 128 or 224 pixel images.

---

## Part 4. The code, block by block

### Block 0. Settings and device

```python
IMG_SIZE = 128
N_TRAIN, N_TEST = 5000, 1000
BATCH = 32
NUM_CLASSES = 10

if torch.cuda.is_available():   device = torch.device("cuda")
elif torch.backends.mps.is_available(): device = torch.device("mps")
else:                           device = torch.device("cpu")
```

- **Device**: where the maths happens (NVIDIA GPU, Apple GPU, or plain CPU). The model **and** every batch of data must live on the same device.
- We use 5,000 training images (not 50,000) and 128 pixels (not 224) so it runs in minutes on a laptop. Make them bigger for better accuracy.

**Recall:** Why do we use `N_TRAIN = 5000` instead of all 50,000 images?
<details><summary>Answer</summary>Speed only. Transfer learning needs much less data than training from scratch, so a small subset still works well, and it keeps the lab fast on a laptop.</details>

### Block 1. Data

```python
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])
trainset = torchvision.datasets.CIFAR10(root='./data', train=True, download=True, transform=transform)
trainset = Subset(trainset, range(N_TRAIN))
trainloader = DataLoader(trainset, batch_size=BATCH, shuffle=True)
```

- `Resize(128)`: CIFAR pictures are 32x32, which is tiny for ResNet. Upscaling gives its layers more room to work.
- `ToTensor()`: image to tensor `[3, H, W]` with values 0-1.
- `Normalize(mean, std)`: `(x - mean) / std` per colour channel. The numbers `[0.485, 0.456, 0.406]` and `[0.229, 0.224, 0.225]` are the **ImageNet** statistics (R, G, B). ResNet was trained on data normalized this way, so we must feed it the same way. In Task 1 we used 0.5/0.5 because our own model had no history.
- `Subset(dataset, range(N))`: take only the first N items.
- Everything else is the same as Task 1.

**Recall:** In Task 1 we normalized with `(0.5, 0.5, 0.5)`. Why do we change it here?
<details><summary>Answer</summary>The pretrained ResNet learned on ImageNet images normalized with the ImageNet mean and std. Giving it differently scaled inputs would be like speaking to it in a language it wasn't taught.</details>

### Block 2. Load the pretrained model

```python
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
```

- Builds ResNet18 and **downloads the trained weights** (about 45 MB, once; cached in `~/.cache/torch`).
- `weights=...DEFAULT` means "the best available pretrained weights".
- Older tutorials write `pretrained=True`. That is deprecated, so use `weights=`.
- Without `weights=`, you would get a randomly initialised ResNet, which is no better than training from scratch.

### Block 3. Freeze

```python
for param in model.parameters():
    param.requires_grad = False
```

- Every weight is a `param`. `requires_grad = True` means "track gradients for this and let the optimizer change it".
- Setting it to `False` means *this weight is locked*. `backward()` won't compute its gradient, so it can't change.
- It also saves time and memory, because PyTorch skips gradient computation for all the frozen layers.

### Block 4. Replace the last layer

```python
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)   # 512 -> 10
model = model.to(device)
```

- `model.fc.in_features` reads the 512 so you don't hard-code it.
- A **brand-new** `nn.Linear` is created **after** freezing, so its `requires_grad` is `True` by default. That is exactly what we want: everything frozen except the new layer.
- Order matters: freeze first, then replace. If you replaced first and then froze everything, you'd freeze the new layer too, and nothing would learn.
- `.to(device)` moves the model to the GPU or CPU.
- Forgetting this step is dangerous because it fails silently. The model still outputs 1000 scores, and since your labels are 0-9, `CrossEntropyLoss` doesn't crash. The model just predicts among the wrong 1000 classes.

**Recall:** Why is only the new `fc` trainable right after Block 4?
<details><summary>Answer</summary>Block 3 set requires_grad=False on all the old parameters. The new Linear layer is created afterwards, and new layers default to requires_grad=True.</details>

### Block 5. Train and evaluate helpers

```python
def train(epochs, optimizer, backbone_trains):
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
```

- The loop body is the **same five steps** as Task 1: zero, forward, loss, backward, step.
- New: `.to(device)` on each batch.
- New: `model.eval()` while the backbone is frozen. ResNet has **BatchNorm** layers that keep running averages while in train mode, *even if their weights are frozen*. In eval mode those averages are fixed, which is what "frozen" should mean. In Phase 2 we use `model.train()` because everything is learning.
- `evaluate()` is the same as Task 1 (`model.eval()`, `torch.no_grad()`, `torch.max(outputs, 1)`, count correct), plus `.to(device)`.

**Recall:** Which line of the loop would you delete if you were only *testing* and not training? Which wrapper would you add?
<details><summary>Answer</summary>Delete zero_grad, loss.backward and optimizer.step (and the loss). Wrap the loop in <code>with torch.no_grad():</code> and call <code>model.eval()</code>.</details>

### Block 6. Phase 1: train only the new layer

```python
optimizer = optim.SGD(model.fc.parameters(), lr=0.001, momentum=0.9)
train(epochs=3, optimizer=optimizer, backbone_trains=False)
evaluate()
```

- `model.fc.parameters()`: give the optimizer **only** the new layer's weights. The others are frozen anyway.
- This is fast, because the frozen layers need no backward pass.

### Block 7. Phase 2: fine-tune everything

```python
for param in model.parameters():
    param.requires_grad = True
optimizer = optim.SGD(model.parameters(), lr=0.0001, momentum=0.9)
train(epochs=2, optimizer=optimizer, backbone_trains=True)
evaluate()
```

- **Unfreeze** all layers.
- **A smaller learning rate (10x smaller)**: the pretrained weights are already good, so we only want gentle nudges. Big steps would wreck them. This is the most important rule of fine-tuning.
- A **new optimizer** is created because the old one only knew about `fc`.

**Recall:** Why a *smaller* learning rate in Phase 2 than in Phase 1?
<details><summary>Answer</summary>The backbone already holds good features. Large updates could destroy them, so we make tiny corrections. The new fc layer started random, so it could afford larger steps in Phase 1.</details>

---

## Part 5. Common mistakes (and how they show up)

| Mistake | Symptom |
|---|---|
| Forgot to replace `fc` | Model has 1000 outputs. No crash, but poor results |
| Used 0.5/0.5 normalization | Lower accuracy than expected |
| Forgot `.to(device)` on the model or data | `RuntimeError: Expected all tensors to be on the same device` |
| Unfroze too early and used a big learning rate | Loss jumps up or accuracy collapses |
| Replaced `fc` before freezing, then froze all | Loss never moves, because nothing is trainable |
| Forgot to build a new optimizer after unfreezing | Backbone doesn't change in Phase 2 |
| Used `pretrained=True` | Deprecation warning (still works in old versions) |

---

## Part 6. Recall and rewrite exercises

### A. Quick questions (answer out loud, then check)

1. What does "freezing" a layer mean in PyTorch? What attribute do you set?
2. After `print(model)`, what is the name and size of ResNet18's final layer?
3. Why do we pass `model.fc.parameters()` to the optimizer in Phase 1?
4. What is `.to(device)` and what two things must you move?
5. What does `torch.max(outputs, 1)` return, and which part is the prediction?
6. What is the difference between feature extraction and fine-tuning?

<details><summary>Answers</summary>

1. The layer's weights are locked and don't update. Set `param.requires_grad = False`.
2. `fc`, a `Linear(512, 1000)`.
3. Only the new layer needs to learn, and giving it only those parameters is explicit and efficient.
4. It moves a tensor or model to the GPU/CPU. Move the model and every batch (images and labels).
5. `(values, indices)`. The index is the predicted class.
6. Feature extraction trains only the new final layer while the backbone stays frozen. Fine-tuning also lets the backbone change, gently.

</details>

### B. Fill in the blanks (close `transfer.py` first)

```python
model = models.resnet18(weights=models.ResNet18_Weights.______)

for param in model.parameters():
    param.______ = False

model.fc = nn.Linear(model.fc.______, 10)

optimizer = optim.SGD(model.______.parameters(), lr=0.001, momentum=0.9)
```

<details><summary>Answers</summary>DEFAULT, requires_grad, in_features, fc</details>

### C. Rewrite from memory (the real test)

Create an empty file. **Without looking**, write:

1. All the imports.
2. The transform (Resize, ToTensor, Normalize with ImageNet numbers) and the loaders.
3. Load, freeze, replace `fc`.
4. The loss, the optimizer, and a training loop.
5. The evaluation loop.

Then compare with `transfer.py`. Mark what you forgot, and rewrite just that part again tomorrow.

### D. Shape check

For input `[32, 3, 128, 128]`, write the shape after `layer2`, after `avgpool`, and after `fc`.
<details><summary>Answer</summary>[32, 128, 16, 16], then [32, 512, 1, 1], then [32, 10]</details>

### E. Variations (to prove you understand it)

1. **CIFAR-100:** change two things. Which? <details><summary>Answer</summary>`datasets.CIFAR100` instead of `CIFAR10`, and `NUM_CLASSES = 100`.</details>
2. **Compare:** train with `requires_grad` never unfrozen (Phase 1 only) and with Phase 2. Write down both accuracies.
3. **Try a different model.** With `models.resnet34` (swap the name and the `Weights` class) nothing else changes. With `models.mobilenet_v2` the last layer is **not** called `fc`, so print the model and find it. Why does that matter?
   <details><summary>Answer</summary>Replacing the wrong attribute leaves the old 1000-class head in place. Always `print(model)` and look at the last layer first.</details>

---

## Part 7. Using a real custom dataset

"Custom dataset" normally means your own folder of images, one subfolder per class:

```
mydata/
  train/
    cats/   img1.jpg, img2.jpg, ...
    dogs/   ...
  test/
    cats/   ...
    dogs/   ...
```

Replace the CIFAR lines in Block 1 with:

```python
trainset = torchvision.datasets.ImageFolder('mydata/train', transform=transform)
testset  = torchvision.datasets.ImageFolder('mydata/test',  transform=transform)
NUM_CLASSES = len(trainset.classes)
```

- `ImageFolder` reads the subfolder names as class names and numbers them 0, 1, 2... alphabetically. Use `trainset.classes` to see them.
- Delete the two `Subset(...)` lines unless you want a smaller dataset.
- Everything else stays the same, which is the point of transfer learning.

---

## Part 8. One-page cheat sheet

```python
# data: resize + ImageNet normalize
transform = Compose([Resize(128), ToTensor(), Normalize(IMAGENET_MEAN, IMAGENET_STD)])

# model
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
for p in model.parameters(): p.requires_grad = False        # freeze
model.fc = nn.Linear(model.fc.in_features, NUM_CLASSES)     # new head
model = model.to(device)

# phase 1: train head only
optimizer = optim.SGD(model.fc.parameters(), lr=1e-3, momentum=0.9)
# loop: zero_grad -> forward -> loss -> backward -> step

# phase 2: fine-tune everything, smaller lr
for p in model.parameters(): p.requires_grad = True
optimizer = optim.SGD(model.parameters(), lr=1e-4, momentum=0.9)
```

**Remember:** keep the features, replace the head, freeze first, then unfreeze with a smaller learning rate.
