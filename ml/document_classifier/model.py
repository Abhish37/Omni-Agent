import tensorflow as tf
from tensorflow.keras import layers, models
import os

class DocumentClassifier:
    def __init__(self, input_shape=(224, 224, 3), num_classes=3):
        """
        num_classes: e.g., 3 (Invoice, Receipt, Spam)
        """
        self.input_shape = input_shape
        self.num_classes = num_classes
        self.model = self._build_model()

    def _build_model(self):
        # Lightweight CNN architecture
        model = models.Sequential([
            layers.Conv2D(32, (3, 3), activation='relu', input_shape=self.input_shape),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.MaxPooling2D((2, 2)),
            
            layers.Conv2D(64, (3, 3), activation='relu'),
            layers.Flatten(),
            
            layers.Dense(64, activation='relu'),
            layers.Dropout(0.5),
            layers.Dense(self.num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer='adam',
            loss='sparse_categorical_crossentropy',
            metrics=['accuracy']
        )
        return model

    def train(self, train_dataset, val_dataset, epochs=10):
        # Placeholder for training logic
        return self.model.fit(
            train_dataset,
            validation_data=val_dataset,
            epochs=epochs
        )

    def save(self, filepath):
        self.model.save(filepath)

    @classmethod
    def load(cls, filepath):
        classifier = cls()
        classifier.model = tf.keras.models.load_model(filepath)
        return classifier
