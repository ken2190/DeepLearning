from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
import numpy as np
import argparse

def signmoid_activation(x):
    return 1/(1+ np.exp(-x))
def predict(X,W):
    preds = signmoid_activation(X.dot(W))
    preds[preds<=0.5] = 0
    preds[preds>0.5]= 1
    return preds
ap = argparse.ArgumentParser()
ap.add_argument("-e","--epochs",type=float, default=100, help="epoch")
ap.add_argument("-a","--alpha",type=float, default=0.01, help="learning rate")
args = vars(ap.parse_args())
(X,y) = make_blobs(n_samples=10000, n_features=2, centers=2,cluster_std= 1.5,random_state=1)

print(X.shape, y.shape)
y = y.reshape((y.shape[0], 1))
print(X.shape, y.shape)
### chèn 1 cột
X = np.c_[X, np.ones((X.shape[0]))]
print(X.shape, y.shape)
(trainX,testX,trainY,testY) = train_test_split(X, y, test_size=0.5,random_state=42)

print("[INFO] training...")
W = np.random.randn(X.shape[1],1) # class labels
losses = []

test_one = 0
for epoch in np.arange(0,args["epochs"]):
    preds = signmoid_activation(trainX.dot(W))        
    error = preds - trainY
    loss = np.sum(error **2)
    losses.append(loss)

    
    gradient = trainX.T.dot(error)

    W += -args["alpha"] * gradient
    
 

    if epoch == 0 or (epoch + 1) % 5 == 0:
        print("[INFO] epoch={}, loss={:.7f}".format(int(epoch + 1),loss))
        print(preds)
        print(trainY)
        print(error)
        
    
print("[INFO] evaluating...")
preds = predict(testX, W)
print(classification_report(testY, preds))
preds = predict(testX, W)
print(classification_report(testY, preds))

plt.style.use("ggplot")
plt.figure()
plt.title("Data")
plt.scatter(testX[:, 0], testX[:, 1], marker="o", c=testY, s=30)

plt.style.use("ggplot")
plt.figure()
plt.plot(np.arange(0, args["epochs"]), losses)
plt.title("Training Loss")
plt.xlabel("Epoch #")
plt.ylabel("Loss")

plt.show()