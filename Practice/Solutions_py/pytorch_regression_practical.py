"""
PyTorch regression practical (instructor-style checklist) - COMPSCI4084

A neural network learns a CONTINUOUS target:  y = X @ w + b + noise.

Checklist covered, one small operation at a time:
    1. set a random seed BEFORE any random numbers are made
    2. generate synthetic data and understand the shapes of X and y
    3. define a simple network with torch.nn.Module (Linear + ReLU)
    4. choose the loss function and the optimiser
    5. basic training loop, recording the loss of every epoch
    6. plot the training loss
    7. evaluate: predictions vs true values, train/test split
    8. sanity check: a single Linear layer recovers w and b
    9. prove the seed makes the run reproducible

Run:  python pytorch_regression_practical.py
(needs torch + matplotlib; set MPLBACKEND=Agg to run without a window)
"""
import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------
# Settings (one place, so you can change them easily in the exam)
# ----------------------------------------------------------------------
SEED = 42              # any whole number; same number = same results
N_SAMPLES = 100        # N: rows (one row = one example)
N_FEATURES = 4         # F: columns (one column = one input measurement)
N_HIDDEN = 16          # neurons in the hidden layer
NOISE_STD = 0.1        # spread of the noise  (noise floor MSE = 0.1**2)
EPOCHS = 200           # number of passes over the data
LEARNING_RATE = 0.05   # size of each adjustment


def make_data(n_samples, n_features, noise_std):
    """Return X (N,F), y (N,1) and the true w (F,1) and b.

    Seed is NOT set in here: the caller sets it first, so the order of
    random numbers (seed -> data -> model) is clear in the main program.
    """
    X = torch.randn(n_samples, n_features)            # (N, F) bell curve
    # the hidden rule the network must discover: 4 weights and a bias.
    # .reshape(F, 1) makes w a COLUMN, so X @ w has shape (N, 1)
    w = torch.tensor([2.0, -1.0, 0.5, 3.0]).reshape(n_features, 1)
    b = 1.5                                            # a plain number
    noise = noise_std * torch.randn(n_samples, 1)      # (N, 1), small
    y = X @ w + b + noise                              # (N,F)@(F,1)->(N,1)
    return X, y, w, b


class RegressionNet(nn.Module):
    """F inputs -> hidden Linear + ReLU -> 1 output (NO activation)."""

    def __init__(self, n_features, n_hidden):
        super(RegressionNet, self).__init__()   # always the first line
        self.fc1 = nn.Linear(n_features, n_hidden)   # F -> hidden
        self.fc2 = nn.Linear(n_hidden, 1)            # hidden -> 1 number

    def forward(self, x):
        x = torch.relu(self.fc1(x))   # hidden layer + ReLU gate
        x = self.fc2(x)               # raw number out: no sigmoid, no relu
        return x


def run_experiment(seed):
    """Whole pipeline, returns the list of epoch losses (used in step 9)."""
    torch.manual_seed(seed)                           # seed FIRST
    X, y, _, _ = make_data(N_SAMPLES, N_FEATURES, NOISE_STD)
    model = RegressionNet(N_FEATURES, N_HIDDEN)       # weights random too
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
    history = []
    for epoch in range(EPOCHS):
        optimizer.zero_grad()
        loss = criterion(model(X), y)
        loss.backward()
        optimizer.step()
        history.append(loss.item())
    return history


# ======================================================================
# 1. SEED  - must come before ANY torch.randn and before creating the model
# ======================================================================
torch.manual_seed(SEED)

# ======================================================================
# 2. DATA  - y = X @ w + b + noise
# ======================================================================
X, y, w_true, b_true = make_data(N_SAMPLES, N_FEATURES, NOISE_STD)
print("X shape:", X.shape)          # torch.Size([100, 4])
print("y shape:", y.shape)          # torch.Size([100, 1])  a column
print("true w :", w_true.flatten().tolist(), " true b:", b_true)

# ======================================================================
# 3. MODEL, 4. LOSS and OPTIMISER
# ======================================================================
model = RegressionNet(N_FEATURES, N_HIDDEN)
print(model)                                  # lists the layers
criterion = nn.MSELoss()                      # continuous target -> MSE
optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)
# SGD alternative: optim.SGD(model.parameters(), lr=0.05) - learns slower

# ======================================================================
# 5. TRAINING LOOP, recording the loss
# ======================================================================
losses = []                                   # the score-book
for epoch in range(EPOCHS):
    optimizer.zero_grad()                     # wipe last round's feedback
    predictions = model(X)                    # forward: sit the quiz
    loss = criterion(predictions, y)          # score = points lost
    loss.backward()                           # teacher marks the paper
    optimizer.step()                          # student adjusts habits
    losses.append(loss.item())                # keep the number
    if (epoch + 1) % 20 == 0 or epoch == 0:   # print every 20th epoch
        print(f"Epoch {epoch + 1:03d} | Loss: {loss.item():.6f}")

print(f"Noise floor is about {NOISE_STD ** 2:.4f}; final loss "
      f"{losses[-1]:.4f}")

# ======================================================================
# 7a. EVALUATE on the training data: predictions vs true values
# ======================================================================
model.eval()                                  # exam-hall mode
with torch.no_grad():                         # no learning, no gradients
    predictions = model(X)
print("first 5 samples:   predicted  vs  true")
for i in range(5):
    print(f"   {predictions[i].item():9.3f}   {y[i].item():9.3f}")

# ======================================================================
# 7b. TRAIN / TEST SPLIT (80 / 20): learn on one part, test on unseen part
# ======================================================================
X_train, X_test = X[:80], X[80:]
y_train, y_test = y[:80], y[80:]
split_model = RegressionNet(N_FEATURES, N_HIDDEN)
split_opt = optim.Adam(split_model.parameters(), lr=LEARNING_RATE)
for epoch in range(EPOCHS):
    split_opt.zero_grad()
    split_loss = criterion(split_model(X_train), y_train)
    split_loss.backward()
    split_opt.step()
split_model.eval()
with torch.no_grad():
    test_loss = criterion(split_model(X_test), y_test).item()
print(f"train MSE {split_loss.item():.4f} | test MSE {test_loss:.4f}")

# ======================================================================
# 8. SANITY CHECK: one Linear(F, 1) layer must recover w and b
# ======================================================================
linear = nn.Linear(N_FEATURES, 1)
lin_opt = optim.SGD(linear.parameters(), lr=0.1)
for epoch in range(200):
    lin_opt.zero_grad()
    lin_loss = criterion(linear(X), y)
    lin_loss.backward()
    lin_opt.step()
print("learned w:", [round(v, 3) for v in linear.weight.flatten().tolist()])
print("true    w:", w_true.flatten().tolist())
print("learned b:", round(linear.bias.item(), 3), "  true b:", b_true)

# ======================================================================
# 9. REPRODUCIBILITY: same seed -> exactly the same loss list
# ======================================================================
run_a = run_experiment(SEED)
run_b = run_experiment(SEED)
run_c = run_experiment(SEED + 1)
print("same seed, same losses?     ", run_a == run_b)       # True
print("different seed, same losses?", run_a == run_c)       # False

# ======================================================================
# 6. PLOT the training loss (last, because plt.show() waits for you)
# ======================================================================
plt.plot(range(1, EPOCHS + 1), losses)
plt.title("Training Loss Over Time")
plt.xlabel("Epoch")
plt.ylabel("Loss (MSE)")
plt.grid(True)
plt.show()
