# ML - Model Training & Inference

Machine learning pipeline for training and using CNN models to detect Rubik's Cube face colors.

## 📋 Requirements

- Python 3.10+
- TensorFlow 2.14+
- See `requirements.txt` for all dependencies

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 🤖 Model Training

### Quick Start (Synthetic Data)

```bash
python train.py
```

This trains on synthetic data (~1200 images, 200 per color) and saves the model to `../models/face_classifier.h5`.

Training time: ~2-5 minutes on CPU, ~1 minute on GPU.

### Training with Real Data

1. **Download Dataset**
   - Get the [Kaggle Rubik's Cube Face Dataset](https://www.kaggle.com/datasets/aryan7004/rubiks-cube-face-dataset/)
   - Extract to `data/rubiks_cube_dataset/`

2. **Update Data Path**
   In `train.py`, change:
   ```python
   train_model(
       dataset_path="data/rubiks_cube_dataset",  # Update this
       use_synthetic=False
   )
   ```

3. **Run Training**
   ```bash
   python train.py
   ```

## 📊 Model Architecture

The CNN (`model.py`) has:
- 3 convolutional blocks
- Batch normalization
- Max pooling layers
- Dropout for regularization
- Dense layers
- Softmax output (6 color classes)

**Input:** 224×224×3 images
**Output:** Probability distribution over 6 colors (W, R, G, B, O, Y)

## 📁 Project Structure

```
ml/
├── train.py           # Training script
├── model.py           # CNN architecture
├── data_loader.py     # Dataset loading
├── inference.py       # Inference utilities
└── requirements.txt
```

## 🎯 Usage

### Training

```python
from train import train_model

model, history = train_model(
    use_synthetic=True,
    epochs=50,
    batch_size=32
)
```

### Inference

```python
from inference import CubeInference
import numpy as np

# Load model
inference = CubeInference("../models/face_classifier.h5")

# Single color prediction
image = np.random.rand(224, 224, 3)  # Load actual image here
color, confidence = inference.predict_color(image)
print(f"Color: {color}, Confidence: {confidence:.2%}")

# Full face prediction (3x3 grid)
face_colors, mean_conf = inference.predict_face(image)
print(f"Face colors:\n{face_colors}")
print(f"Mean confidence: {mean_conf:.2%}")
```

## 📈 Training Process

1. **Data Loading**
   - Loads images from dataset or generates synthetic data
   - Splits into train/val (80/20)
   - Normalizes to [0, 1]

2. **Model Training**
   - Uses Adam optimizer
   - Categorical crossentropy loss
   - Tracks accuracy metric
   - Early stopping if no improvement
   - Learning rate reduction on plateau

3. **Model Saving**
   - Saves to `../models/face_classifier.h5`
   - In H5 format (Keras native)

## 🔧 Configuration

Modify `train.py` for:
- Number of epochs
- Batch size
- Learning rate (in model.py)
- Dropout rates
- Dataset path

## 📊 Color Classes

Model predicts 6 colors:
| Index | Color  | Letter | RGB |
|-------|--------|--------|-----|
| 0     | White  | W      | 255,255,255 |
| 1     | Red    | R      | 255,0,0     |
| 2     | Green  | G      | 0,255,0    |
| 3     | Blue   | B      | 0,0,255    |
| 4     | Orange | O      | 255,165,0  |
| 5     | Yellow | Y      | 255,255,0  |

## 🧪 Evaluation

After training, evaluate on validation set:

```python
from train import train_model

model, history = train_model()

# Access training history
print(f"Final accuracy: {history.history['accuracy'][-1]:.2%}")
print(f"Final val_accuracy: {history.history['val_accuracy'][-1]:.2%}")
```

## 🚀 Optimization

### For Production
- Quantize model (reduce size by ~75%)
- Use TF Lite for mobile
- Batch predictions for speed

### For Training Speed
- Use GPU (CUDA + cuDNN)
- Increase batch size
- Use mixed precision training

## 📦 Model Formats

The model is saved in H5 format. To convert:

```python
import tensorflow as tf

# Load H5 model
model = tf.keras.models.load_model("face_classifier.h5")

# Convert to TF Lite (for mobile)
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save
with open("face_classifier.tflite", "wb") as f:
    f.write(tflite_model)
```

## 📊 Dataset Info

### Kaggle Dataset
- Contains labeled Rubik's Cube face images
- Multiple colors well-represented
- Various lighting conditions

### Synthetic Dataset
- Generated for testing/CI
- Simple color blocks with noise
- 200 images per color (1200 total)

## 🔄 Continuous Training

The GitHub Actions workflow (`ml-training.yml`) can automatically:
1. Train the model on new commits
2. Save trained model as artifact
3. Potentially upload to cloud storage

## 🐛 Troubleshooting

1. **Out of Memory**: Reduce batch size or image size
2. **Low Accuracy**: 
   - Check dataset quality
   - Increase epochs
   - Adjust learning rate
3. **Model Too Large**: Quantize or use a smaller base model

## 📈 Performance Metrics

Expected performance with full dataset:
- Accuracy: 95%+
- Inference time: 50-100ms per image (CPU)
- Model size: ~20-50 MB (unquantized)

## 📄 License

See LICENSE in root directory
