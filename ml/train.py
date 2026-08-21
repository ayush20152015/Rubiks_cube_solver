"""
Training script for Rubik's Cube color classification CNN
"""
import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from model import CubeColorCNN
from data_loader import CubeDataLoader


def train_model(
    dataset_path: str = None,
    model_save_path: str = "../models/face_classifier.h5",
    use_synthetic: bool = True,
    epochs: int = 50,
    batch_size: int = 32
):
    """
    Train CNN model for cube face classification
    
    Args:
        dataset_path: Path to Kaggle dataset (if not using synthetic data)
        model_save_path: Where to save trained model
        use_synthetic: Use synthetic data for testing if True
        epochs: Number of training epochs
        batch_size: Batch size
    """
    print("Loading data...")
    data_loader = CubeDataLoader(dataset_path or ".")
    
    if use_synthetic:
        print("Using synthetic dataset...")
        x_data, y_data = data_loader.load_sample_dataset(num_samples=200)
    else:
        print("Loading Kaggle dataset...")
        x_data, y_data = data_loader.load_kaggle_dataset()
    
    print(f"Dataset shape: {x_data.shape}, Labels shape: {y_data.shape}")
    
    # Convert labels to one-hot encoding
    y_data_encoded = to_categorical(y_data, num_classes=6)
    
    # Train/val split
    x_train, x_val, y_train, y_val = train_test_split(
        x_data, y_data_encoded,
        test_size=0.2,
        random_state=42
    )
    
    print(f"Training set size: {x_train.shape[0]}, Validation set size: {x_val.shape[0]}")
    
    # Build and train model
    print("Building model...")
    model = CubeColorCNN()
    
    print("Training model...")
    history = model.train(
        x_train, y_train,
        x_val, y_val,
        epochs=epochs,
        batch_size=batch_size
    )
    
    # Save model
    os.makedirs(os.path.dirname(model_save_path), exist_ok=True)
    model.save(model_save_path)
    
    print("Training complete!")
    return model, history


if __name__ == "__main__":
    train_model(
        use_synthetic=True,  # Set to False when using real Kaggle dataset
        epochs=10,  # Reduced for MVP
        batch_size=32
    )
