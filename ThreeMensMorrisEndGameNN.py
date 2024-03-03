import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
import pandas as pd


X = np.load("x1.npy")
y = np.load("y1.npy")

y = keras.utils.to_categorical(y)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

model = Sequential([
    Conv2D(filters=128, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Conv2D(filters=64, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='tanh'),
    Dense(16, activation='relu'),
    Dense(units=2, activation='softmax')  # 3 output units for the three classes
])
model.compile(
      optimizer='Adam',
      loss='categorical_crossentropy',
      metrics=['accuracy']
   )

history = model.fit(
      x=x_train,
      y=y_train,
      epochs=10,
      shuffle=True
   )

score = model.evaluate(x_test, y_test, verbose=0)
score_train = model.evaluate(x_train, y_train, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

state = np.array([[1, 1, 1],
                  [0, -1, 0],
                  [-1, 0, -1]])
state2 = np.array([[-1, -1, -1],
                  [0, 1, 0],
                   [0, 1, 1]])
state3 = np.array([[1, 0, -1],
                  [1, -1, 0],
                  [1, 0, -1]])

state = state.reshape(-1, 3, 3)
state = state.reshape((-1, 3, 3, 1))
state2 = state2.reshape(-1, 3, 3)
state2 = state2.reshape((-1, 3, 3, 1))
state3 = state3.reshape(-1, 3, 3)
state3 = state3.reshape((-1, 3, 3, 1))
answer = model.predict([state])
answer2 = model.predict([state2])
answer3 = model.predict([state3])

print(answer, "succeed?")
print(answer2, "succeed?")
print(answer3, "succeed?")
print(history.history.keys())
acc = history.history['accuracy']
print("accuracy - train", score_train[1])

loss = history.history['loss']

epochs = range(1, len(acc)+1)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.plot(epochs, acc, 'bo', label='Training acc')

plt.title('Training  accuracy')
plt.legend()
plt.show()

model.save('saved model.keras')
model1 = keras.models.load_model('saved model.keras')
