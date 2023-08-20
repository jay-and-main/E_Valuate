import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
#import emnist
from extra_keras_datasets import emnist


#mnist= tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = emnist.load_data(type='letters')

#Split to trainig data and testing data

x_train = tf.keras.utils.normalize(x_train,axis=1)
x_test = tf.keras.utils.normalize(x_test,axis=1)

#1 input layer,2 hidden layers,1 output layer

#Normalise RGB and Grayscale to 0 and 1

model= tf.keras.models.Sequential() #Basic neural network
model.add(tf.keras.layers.Flatten(input_shape=(28,28)))  #New layer(flatten for 1 dimensional)

model.add(tf.keras.layers.Dense(units=128,activation=tf.nn.relu)) #rectify linear unit
model.add(tf.keras.layers.Dense(units=128,activation=tf.nn.relu)) #To connect the neural layers

model.add(tf.keras.layers.Dense(units=50,activation=tf.nn.softmax))#Scales the probability

#To find the probabilty of a specific handwritten element

model.compile(optimizer='adam',loss='sparse_categorical_crossentropy',metrics=['accuracy'])
#Optimizer-->Algorithm to change attributes of neural network. Adam uses a gradient
#Loss--> Prediction and calculation of error


model.fit(x_train,y_train,epochs=5)  #To train the model(epochs-->reptition of model)

accuracy,loss=model.evaluate(x_test,y_test)
print(accuracy)
print(loss)

model.save('digits.model') #To prevent training repeatedly


def E_valuate():
    lst=[]
    i=0
    while True:
      try:
        img = cv2.imread(f'D:/Class 12 CS/CS Project/Images1/{i}.png')[:,:,0]
        img = np.array([img])
        prediction = model.predict(img)
        result=int(np.argmax(prediction))
        lst.append(result)
        #plt.imshow(img[0],cmap = plt.cm.binary)
        plt.show()
        i+=1
      except:
        break
    print(lst)
    #Check each letter since output is a number of range [1,26]
    letter_list=[]
    j=0
    while j<len(lst):
      if lst[j]==1:
        letter_list.append('A')
      if lst[j]==2:
        letter_list.append('B')
      if lst[j]==3:
        letter_list.append('C')
      if lst[j]==4:
        letter_list.append('D')
      if lst[j]==5:
        letter_list.append('E')
      if lst[j]==6:
        letter_list.append('F')
      if lst[j]==7:
        letter_list.append('G')
      if lst[j]==8:
        letter_list.append('H')
      if lst[j]==9:
        letter_list.append('I')
      if lst[j]==10:
        letter_list.append('J')
      if lst[j]==11:
        letter_list.append('K')
      if lst[j]==12:
        letter_list.append('L')
      if lst[j]==13:
        letter_list.append('M')
      if lst[j]==14:
        letter_list.append('N')
      if lst[j]==15:
        letter_list.append('O')
      if lst[j]==16:
        letter_list.append('P')
      if lst[j]==17:
        letter_list.append('Q')
      if lst[j]==18:
        letter_list.append('R')
      if lst[j]==19:
        letter_list.append('S')
      if lst[j]==20:
        letter_list.append('T')
      if lst[j]==21:
        letter_list.append('U')
      if lst[j]==22:
        letter_list.append('V')
      if lst[j]==23:
        letter_list.append('W')
      if lst[j]==24:
        letter_list.append('X')
      if lst[j]==25:
        letter_list.append('Y')
      if lst[j]==26:
        letter_list.append('Z')
      j+=1
    print(letter_list)
    return letter_list
'''
l=random()
s=''
for i in l:
    s+=i
print(s)
'''
