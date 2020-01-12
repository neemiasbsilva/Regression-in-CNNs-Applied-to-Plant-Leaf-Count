# -*- coding: utf-8 -*-
"""NasNetLarge.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1uCGExlKhQbUx33CnxO1YImsz5lckraZO

# Importando as bibliotecas para utilizar na Rede Neural Convolucional

*   **Primeiro:** vamos importa a biblioteca numpy para fazer alguns cálculos científicos
*   **Segundo:** vamos importar as bibliotecas os e csv para abrir o nosso arquivo para utilizarmos as nossas imagens.
*   **Terceiro:** vamos importar as bibliotecas "skimage" para poder fazer manipulação na imagem
*   **Quarto:** vamos importar o modelo "Sequential" para utilizar o keras como camada feed-foward.
*   **Quindo** vamos importar a biblioteca "Matplotlib" para plotarmos a imagen que estamos utilizando.
"""

import numpy as np
import os
import csv 
from skimage import io, transform
import matplotlib.pyplot as plt

"""# Importando o google drive para montar e conseguir treinar as imagens


1.   Será preciso importar a biblioteca *drive*;
2.   Depois será preciso montar o arquivo para que possa utilizar o google drive como caminho
"""

from google.colab import drive
drive.mount('/content/drive/')

"""# Após montar o drive vamos implementar algumas funções para podermos pegar as nossas imagens. Abaixo segue especificando cada uma delas:


1.   **Abrir o arquivo csv:** para abrir o arquivo .csv implementamos uma função;
2.   **Abrir as imagens:** para abrir as imagens implementamos uma função que tem como base o arquivo .csv
3.   **Mudar o número das classes:** como as classes não começa com uma orde foi necessário escalar as imagens para que ficassem em uma escala entre zero até a classe mais alta que do zero ao 29;
"""

def openCsv(wayFile):
    way_classes = []
    way_datas = []
    
    count = 0
    
    with open(wayFile, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            way_datas.append(row[0])
            way_classes.append(int(row[1]))
    return way_datas, way_classes
  
def openImage(way_path, way_image, width, height):
    X = []
    for i in range(0, len(way_image)):
        img = io.imread('%s%s' % (way_path, way_image[i]))
        img = img[...,:3]
        img = transform.resize(img,(width, height))
        X.append(img)
    return X
  
def map_classes(way_classes):
    m = {}
    y = np.zeros(len(way_classes))
    uc = np.unique(way_classes)
    
    for i in range(0, len(uc)):
        m[uc[i]] = i
    
    for i in range(0, len(way_classes)):
        y[i] = m[way_classes[i]]
        
    return y, m, uc

"""# Rodando as funções - openCsv(), openImage() e map_classes().



> Nesta Seção será executado as funções que implementamos, para isso definiremos a altura e largura das imagens para que ambas ficam com tamanho padrão.



*   **OBS.:** Transformaremos a lista X_data e y_layers em **array**; as imagens terão 229 de **largura** e 229 de **altura** pois a arquitetura que utilizaremos para que funcione de forma eficiente é necessário que utilizemos as imagens com está redimensão.
"""

#if achiteture is Inception
#width = 299
#height = 299
#If achitecture is NasNet 331 331 3
width = 331
height = 331
#If achitecture is VGG 224 224 3
#width = 224
#height = 224
#If achitecture is Xception 299 299 3
#width = 299
#height = 299
#ResNet50 is 244 224 3
#width = 224
#height = 224


way_path = '/content/drive/My Drive/ColabNotebooks/A1_A2_A3_A4/'
way_image, way_classes = openCsv('/content/drive/My Drive/ColabNotebooks/A1_A2_A3_A4.csv')
X_datas = openImage(way_path, way_image, width, height)
#y_layers, m, uc = map_classes(way_classes)
y_layers = way_classes
X_datas = np.asarray(X_datas)
y_layers = np.asarray(y_layers)


print(y_layers.shape)
print(y_layers)

"""# Agora vamos importar as bibliotecas e modelos que utilizaremos na nossa Rede Neural

*   **Modelo**: Sequencial;
*  **Camadas**: Convolution2D, MaxPooling2D; Dropout, Flatten, Dense
*   **Utilidas**: np_utils
"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.utils import np_utils
from keras.optimizers import RMSprop, SGD, Adam

"""# Nesta Seção vamos dividir o nosso conjunto de dados em conjunto de traino e validação.

*   **Sklearn**: utilizaremos esta biblioteca para dividirmos o conjunto de treinamento aleatóriamente;

# Depois de dividirmos em conjunto de treinamento e validação vamos transformar o vetor de classes.

> Para fazer isso utilizaremos a biblioteca np_utils para transformar o vetor de classes para uma matriz de classes binárias.
> O tamanho da matriz será a quantidade únicas de classes.
"""

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(X_datas, y_layers, test_size=0.20, random_state=42)

x_train, x_val, y_train, y_val = train_test_split(x_train, y_train, test_size=0.20, random_state=42)

x_train = x_train.astype('float32')
x_val = x_val.astype('float32')
x_test = x_test.astype('float32')

#x_train = x_train.reshape(x_train.shape[0], 1, x_train.shape[1], x_train.shape[2]))
#x_val = x_val.reshape((x_val.shape[0], 1, x_val.shape[1], x_val.shape[2]))

#y_train = np_utils.to_categorical(y_train, len(uc))
#Y_test = np_utils.to_categorical(y_test, len(uc))
#y_val = np_utils.to_categorical(y_val, len(uc))

print(X_datas.shape)
print(x_train.shape)
print(x_test.shape)
print(x_val.shape)
#print(np.asarray(range(len(uc))))
#print(y_val[0,:])

"""# Implementation Convolution Neural Network with Xception"""

from keras.applications.nasnet import NASNetLarge
from keras.models import Model

model = NASNetLarge(weights='imagenet', include_top=True, input_shape=(331, 331, 3))

x = model.get_layer(index=len(model.layers)-2).output

print(x)
x = Dense(1)(x)

model = Model(inputs=model.input, outputs=x)
model.summary()

opt = RMSprop(lr=0.0001)
model.compile(loss='mean_squared_error', optimizer=opt, metrics=['mae'])

network_history = model.fit(x_train, y_train, batch_size=8, epochs=100, verbose=1, validation_data= (x_val, y_val))

"""# Salvar o Modelo NasNet"""

#model.save('/content/drive/My Drive/ColabNotebooks/AllmodeloRMSpropXception.h5')

model.save('/content/drive/My Drive/ColabNotebooks/NasNet/modelNasNet.h5')

"""# Carregar o Modelo NasNet"""

from keras.models import load_model

#model = load_model('/content/drive/My Drive/ColabNotebooks/AllmodeloRMSpropXception.h5')

model = load_model('/content/drive/My Drive/ColabNotebooks/NasNet/modelNasNet.h5')

"""# Predict to Inception Xception -- RMSprop

**All of set text**
"""

predictTest = model.predict(x_test, verbose=1)
predictTest = predictTest.reshape(predictTest.shape[0])
#predictTest = predictTest.astype('int32')
#print(x_test.shape)
#print(predictTest.shape)
#print(y_test.shape)
#print(np.round(predictTest))
#print(y_test)
#print(predictTest)

mae = np.abs(y_test - predictTest)
#print(mae)
pos = np.argsort(mae)

print(pos[-1])
print(pos[-2])
print(pos[-3])

#As três imagens piores preditas.
print("\tAs tres imagens que estao piores preditas")
img1 = plt.imshow(x_test[pos[-1]], interpolation='none')
plt.show()
print("Ground Truth: ",y_test[pos[-1]])
print("Prediceted: ",predictTest[pos[-1]])

img2 = plt.imshow(x_test[pos[-2]], interpolation='nearest')
plt.show()
print("Ground Truth: ",y_test[pos[-2]])
print("Prediceted: ",predictTest[pos[-2]])

img3 = plt.imshow(x_test[pos[-3]], interpolation='nearest')
plt.show()
print("Ground Truth: ",y_test[pos[-3]])
print("Prediceted: ",predictTest[pos[-3]])

#As três imagens que estao melhores preditas.
print("\tAs tres imagens que estao melhores preditas")
img1 = plt.imshow(x_test[pos[1]], interpolation='nearest')
plt.show()
print("Ground Truth: ",y_test[pos[1]])
print("Prediceted: ",predictTest[pos[1]])

img2 = plt.imshow(x_test[pos[2]], interpolation='nearest')
plt.show()
print("Ground Truth: ",y_test[pos[2]])
print("Prediceted: ",predictTest[pos[2]])

img3 = plt.imshow(x_test[pos[3]], interpolation='nearest')
plt.show()
print("Ground Truth: ",y_test[pos[3]])
print("Prediceted: ",predictTest[pos[3]])

"""**All of set train**"""

predictTrain = model.predict(x_train, verbose=1)
predictTrain = predictTrain.reshape(predictTrain.shape[0])
#predictTrain = predictTrain.astype('int32')
print(x_train.shape)
print(predictTrain.shape)
print(y_train.shape)
print(np.round(predictTrain))
print(y_train)

"""**All of set validation**"""

predictVal = model.predict(x_val, verbose=1)
predictVal = predictVal.reshape(predictVal.shape[0])
#predictVal = predictVal.astype('int32')
print(x_val.shape)
print(predictVal.shape)
print(y_val.shape)
print(np.round(predictVal))
print(y_val)

"""# Metrics About Xception -- RMSprop

**Metrics "Mean squared error", "Median absolute error",  "R² score" Train**
"""

from sklearn.metrics import r2_score, median_absolute_error, mean_squared_error

y_true = y_train
predict = predictTrain

r2 = r2_score(y_true, predict)
mae = median_absolute_error(y_true, predict)
mse = mean_squared_error(y_true, predict)
print("MSE \t MAE \t R2")
print(mse, "\t", mae,"\t", r2)

from sklearn.metrics import r2_score, median_absolute_error, mean_squared_error

y_true = y_val
predict = predictVal

r2 = r2_score(y_true, predict)
mae = median_absolute_error(y_true, predict)
mse = mean_squared_error(y_true, predict)
print("MSE \t MAE \t R2")
print(mse, "\t", mae,"\t", r2)

"""**R² score**"""

from sklearn.metrics import r2_score

y_true = y_train
predict = predictTrain

r2_score(y_true, predict)

"""**MAE score**"""

from sklearn.metrics import median_absolute_error

y_true = y_train
#y_true = y_true.astype('float32')
predict = predictTrain

median_absolute_error(y_true, predict)

"""**Mean Squared Error -- score**"""

from sklearn.metrics import mean_squared_error


y_true = y_train
predict = predictTrain

mean_squared_error(y_true, predict)

"""**Metrics "Mean squared error", "Median absolute error",  "R² score" Validation**

**R² score**
"""

from sklearn.metrics import r2_score

y_true = y_val
predict = predictVal

r2_score(y_true, predict)

"""**MAE score**"""

from sklearn.metrics import median_absolute_error

y_true = y_val
predict = predictVal

median_absolute_error(y_true, predict)

"""**Mean Squared Error -- score**"""

from sklearn.metrics import mean_squared_error


y_true = y_val
predict = predictVal

mean_squared_error(y_true, predict)

"""**Metrics "Mean squared error", "Median absolute error",  "R² score" Test**

**R² score**
"""

from sklearn.metrics import r2_score

y_true = y_test
predict = predictTest

r2_score(y_true, predict)

"""**MAE score**"""

from sklearn.metrics import median_absolute_error

y_true = y_test
predict = predictTest

median_absolute_error(y_true, predict)

"""**Mean Squared Error -- score**"""

from sklearn.metrics import mean_squared_error


y_true = y_test
predict = predictTest

mean_squared_error(y_true, predict)

"""# Implementando scatter"""

import matplotlib.pyplot as plt


N = y_test.shape
x = predictTest
y = y_test
colors = y_test
#area = np.pi * (10 * np.random.rand(162))**2  # 0 to 15 point radii
area = 80
#plt.title("\nXception\n", fontsize=18)
plt.xlabel("\nPredicted\n", fontsize=12)
plt.ylabel("\nGround Truth\n", fontsize=12)
marker_size=15
#plasma viridis hot
plt.scatter(x, y, s=area, c=colors, cmap='cool', alpha=0.5)
plt.gca().set_axis_bgcolor('white')

cbar= plt.colorbar()
cbar.set_label("Number of Leaves", labelpad=+1)

plt.show()
