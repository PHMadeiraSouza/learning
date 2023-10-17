import tensorflow
from tensorflow import keras
import matplotlib.pyplot as plt
dataset =  keras.datasets.fashion_mnist

print("loading dataset...")
(imag_treino, ident_treino),(imag_test, ident_test) = dataset.load_data()

nomes_ident = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat", 
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]