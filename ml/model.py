import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from typing import Tuple


class CubeColorCNN:
    """
    CNN model for classifying Rubik's Cube face colors
    
    Predicts colors for each 3x3 cell in a cube face
    """
    
    def __init__(self, input_shape: Tuple[int, int, int] = (224, 224, 3)):
        """
        Initialize CNN model
        
        Args:
            input_shape: Input image shape
        """
        self.input_shape = input_shape
        self.model = self._build_model()
    
    def _build_model(self) -> keras.Model:
        """
        Build CNN architecture
        
        Returns:
            Compiled Keras model
        """
        model = keras.Sequential([
            # Block 1
            layers.Conv2D(32, 3, activation='relu', padding='same', 
                         input_shape=self.input_shape, name='conv1_1'),
            layers.BatchNormalization(),
            layers.Conv2D(32, 3, activation='relu', padding='same', name='conv1_2'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, name='pool1'),
            layers.Dropout(0.25),
            
            # Block 2
            layers.Conv2D(64, 3, activation='relu', padding='same', name='conv2_1'),
            layers.BatchNormalization(),
            layers.Conv2D(64, 3, activation='relu', padding='same', name='conv2_2'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, name='pool2'),
            layers.Dropout(0.25),
            
            # Block 3
            layers.Conv2D(128, 3, activation='relu', padding='same', name='conv3_1'),
            layers.BatchNormalization(),
            layers.Conv2D(128, 3, activation='relu', padding='same', name='conv3_2'),
            layers.BatchNormalization(),
            layers.MaxPooling2D(2, name='pool3'),
            layers.Dropout(0.25),
            
            # Global pooling and dense layers
            layers.GlobalAveragePooling2D(),
            layers.Dense(256, activation='relu', name='dense1'),
            layers.BatchNormalization(),
            layers.Dropout(0.5),
            
            # Output: 6 classes (W, R, G, B, O, Y)
            layers.Dense(6, activation='softmax', name='output')
        ])
        
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model
    
    def train(self,
              x_train: np.ndarray,
              y_train: np.ndarray,
              x_val: np.ndarray,
              y_val: np.ndarray,
              epochs: int = 50,
              batch_size: int = 32) -> keras.callbacks.History:
        """
        Train the model
        
        Args:
            x_train: Training images
            y_train: Training labels (one-hot encoded)
            x_val: Validation images
            y_val: Validation labels
            epochs: Number of epochs
            batch_size: Batch size
            
        Returns:
            Training history
        """
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=10,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            )
        ]
        
        history = self.model.fit(
            x_train, y_train,
            validation_data=(x_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1
        )
        
        return history
    
    def save(self, path: str):
        """Save model to file"""
        self.model.save(path)
        print(f"Model saved to {path}")
    
    def load(self, path: str):
        """Load model from file"""
        self.model = keras.models.load_model(path)
        print(f"Model loaded from {path}")
    
    def predict(self, x: np.ndarray) -> np.ndarray:
        """
        Make predictions
        
        Args:
            x: Input images
            
        Returns:
            Predictions
        """
        return self.model.predict(x)
