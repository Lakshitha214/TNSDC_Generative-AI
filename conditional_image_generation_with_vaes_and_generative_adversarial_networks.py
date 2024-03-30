# -*- coding: utf-8 -*-
"""Conditional Image Generation with VAEs and Generative Adversarial Networks.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14Z5lZTOyLnukRvrb4gl_bFNhSRPFfMvE
"""

import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from tensorflow.keras import layers

latent_dim = 100  # Dimensionality of the latent space
num_classes = 10  # Number of classes (e.g., for MNIST)

def build_generator():
    model = keras.Sequential([
        layers.Dense(7 * 7 * 128, input_dim=latent_dim + 10),  # Concatenate latent vector with label info
        layers.LeakyReLU(alpha=0.2),
        layers.Reshape((7, 7, 128)),
        layers.Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'),
        layers.LeakyReLU(alpha=0.2),
        layers.Conv2DTranspose(128, (4,4), strides=(2,2), padding='same'),
        layers.LeakyReLU(alpha=0.2),
        layers.Conv2D(1, (7,7), activation='sigmoid', padding='same')
    ])
    return model


def build_discriminator():
    model = keras.Sequential([
        layers.Conv2D(64, (3, 3), strides=(2, 2), padding='same', input_shape=(28, 28, 1 + num_classes)),
        layers.LeakyReLU(alpha=0.2),
        layers.Conv2D(128, (3, 3), strides=(2, 2), padding='same'),
        layers.LeakyReLU(alpha=0.2),
        layers.Flatten(),
        layers.Dropout(0.4),
        layers.Dense(1, activation='sigmoid')
    ])
    return model


def build_cvae(encoder, generator):
    class Sampling(layers.Layer):
        def call(self, inputs):
            mean, log_var = inputs
            epsilon = keras.backend.random_normal(shape=tf.shape(mean))
            return mean + keras.backend.exp(0.5 * log_var) * epsilon

    image_input = layers.Input(shape=(28, 28, 1))
    label_input = layers.Input(shape=(10,))
    x = layers.Conv2D(64, (3, 3), strides=(2, 2), padding='same')(image_input)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Conv2D(128, (3, 3), strides=(2, 2), padding='same')(x)
    x = layers.LeakyReLU(alpha=0.2)(x)
    x = layers.Flatten()(x)

    z_mean = layers.Dense(latent_dim)(x)
    z_log_var = layers.Dense(latent_dim)(x)
    z = Sampling()([z_mean, z_log_var])
    z_cond = layers.concatenate([z, label_input])

    generated_image = generator(z_cond)
    outputs = encoder(generated_image)

    cvae = keras.Model(inputs=[image_input, label_input], outputs=outputs, name='cvae')
    return cvae

    class Sampling(layers.Layer):
        def call(self, inputs):
           mean, log_var = inputs
           epsilon = self.add_weight(shape=tf.shape(mean),
                                  initializer='random_normal',
                                  stddev=0.01)
           return mean + tf.exp(0.5 * log_var) * epsilon

import tensorflow as tf

class Sampling(layers.Layer):
    def call(self, inputs):
        mean, log_var = inputs
        epsilon = keras.backend.random_normal(shape=tf.shape(mean))
        return mean + keras.backend.exp(0.5 * log_var) * epsilon


generator = build_generator()

# Generate some random latent vectors and labels
num_samples = 10
random_latent_vectors = np.random.normal(size=(num_samples, latent_dim))
random_labels = np.eye(num_classes)[np.random.choice(num_classes, num_samples)]

# Concatenate latent vectors with labels
latent_vectors_with_labels = np.concatenate([random_latent_vectors, random_labels], axis=1)

# Generate images using the generator
generated_images = generator.predict(latent_vectors_with_labels)

# Display the generated images
plt.figure(figsize=(10, 10))
for i in range(num_samples):
    plt.subplot(1, num_samples, i + 1)
    plt.imshow(generated_images[i, :, :, 0], cmap='gray')
    plt.axis('off')
plt.show()