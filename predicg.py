import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
import pandas as pd

print("l")

model = keras.models.load_model('saved model.keras')

state = np.array([[2, 2, 2],
                  [0, 1, 0],
                  [1, 0, 1]])
state2 = np.array([[1, 1, 1],
                  [0, 2, 0],
                   [0, 2, 2]])
state3 = np.array([[2, 0, 1],
                  [2, 1, 0],
                  [2, 0, 1]])

state = state.reshape(-1, 3, 3)
state = state.reshape((-1, 3, 3, 1))
state2 = state2.reshape(-1, 3, 3)
state2 = state2.reshape((-1, 3, 3, 1))
state3 = state3.reshape(-1, 3, 3)
state3 = state3.reshape((-1, 3, 3, 1))

answer = model.predict([state])
answer2 = model.predict([state2])
answer3 = model.predict([state3])

print(answer)
print(answer2)
print(answer3)

print(state)
print(state2)
print(state3)