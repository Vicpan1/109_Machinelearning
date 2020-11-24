  
from os import listdir
from os.path import isfile, isdir, join
import pickle

mypath = "games/arkanoid/log"
files = listdir(mypath)
data = []

for f in files:
    fullpath = join(mypath, f)
    loadFile = open(fullpath, "rb")
    data.append(pickle.load(loadFile))
    loadFile.close()
print("train: " + str(len(data)) + " logs")
frame = []
status = []
ballPosition = []
platformPosition = []
bricks = []

for i in range(0, len(data)):
    for j in range(0, len(data[i])):
        frame.append(data[i][j].frame)
        status.append(data[i][j].status)
        ballPosition.append(data[i][j].ball)
        platformPosition.append(data[i][j].platform)
        bricks.append(data[i][j].bricks)
        
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import numpy as np

platX = np.array(platformPosition)[:, 0][:, np.newaxis]
platX_next = platX[1:, :]
instruct = (platX_next-platX[0: len(platX_next), 0][ :, np.newaxis])/5

ballarray = np.array(ballPosition[: -1])
ball_next = np.array(ballPosition[1:])
x = np.hstack((ballarray, ball_next, platX[: -1, 0][:, np.newaxis]))

y = instruct
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1, random_state = 0)

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(x_train, y_train)

y_knn = neigh.predict(x_test)

filename = "knn.sav"
pickle.dump(neigh, open(filename, 'wb'))