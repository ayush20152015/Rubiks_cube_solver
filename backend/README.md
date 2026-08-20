# Backend - Rubik's Cube Solver API

FastAPI-based REST API for cube face analysis and solving.

## 📋 Requirements

- Python 3.10+
- See `requirements.txt` for all dependencies

## 🚀 Installation

```bash
pip install -r requirements.txt
```

## 🏃 Running the Server

```bash
python main.py
```

Server starts on `http://localhost:8000`

## 📚 API Endpoints

### 1. Upload Face Image
```
POST /api/v1/cube/upload-face
```
Upload an image for a specific cube face.

**Parameters:**
- `image` (multipart): Image file
- `face_id` (form): Face index (0-5)
  - 0 = UP (White)
  - 1 = FRONT (Red)
  - 2 = RIGHT (Blue)
  - 3 = BACK (Orange)
  - 4 = LEFT (Green)
  - 5 = DOWN (Yellow)

**Response:**
```json
{
  "face_id": 0,
  "face_name": "UP",
  "colors": [["W", "W", "W"], ["W", "W", "W"], ["W", "W", "W"]],
  "success": true
}
```

### 2. Solve Cube
```
POST /api/v1/cube/solve
```
Solves the cube with all uploaded faces.

**Response:**
```json
{
  "moves": ["R", "U", "Rprime", "Uprime", ...],
  "cube_state": { "U": [...], "D": [...], ... },
  "success": true
}
```

### 3. Reset Cube
```
POST /api/v1/cube/reset
```
Resets the cube to initial state.

**Response:**
```json
{
  "message": "Cube reset successfully",
  "success": true
}
```

### 4. Get Cube State
```
GET /api/v1/cube/state
```
Returns current cube state.

**Response:**
```json
{
  "cube_state": {
    "U": [...],
    "D": [...],
    "F": [...],
    "B": [...],
    "L": [...],
    "R": [...]
  },
  "success": true
}
```

### 5. Health Check
```
GET /api/v1/cube/health
```
Check API and model status.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

## 📁 Project Structure

```
backend/
├── main.py                  # FastAPI application
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
│
├── routes/
│   ├── __init__.py
│   └── cube.py            # Cube endpoints
│
└── services/
    ├── __init__.py
    ├── image_processor.py  # Image preprocessing
    ├── model_inference.py  # CNN model inference
    └── cube_solver.py      # Cube solving logic
```

## 🔧 Configuration

Edit `config.py` to customize:
- API title and version
- CORS origins (allowed frontend URLs)
- Model paths
- Image preprocessing settings
- Cube solver type

Example CORS configuration:
```python
CORS_ORIGINS: list[str] = [
    "http://localhost:5173",           # Local dev
    "http://localhost:3000",           # Alternative local
    "https://yourvercel-url.com"       # Production
]
```

## 🤖 Services

### ImageProcessor
Handles image loading and preprocessing:
- Loads image from bytes
- Resizes to model input size (224×224)
- Normalizes to [-1, 1]
- Extracts 3×3 color grid using color detection

### ModelInference
Handles CNN model:
- Loads pre-trained model
- Runs inference on images
- Returns color predictions

### CubeSolver
Solves the cube:
- Stores 6 face states
- Validates cube (9 of each color)
- Generates solution move sequence
- Returns final cube state

## 🧪 Testing

Create `tests/` directory with pytest tests:

```bash
pytest
```

## 📝 Environment Variables

Create `.env` file:

```
PYTHONUNBUFFERED=1
DEBUG=False
MODEL_DIR=./models
```

## 🔄 CORS Configuration

The API is configured to accept requests from:
- `http://localhost:5173` (local React dev server)
- `http://localhost:3000` (alternative local)

Update `config.py` for your deployment URLs.

## 🚢 Deployment

### Docker
Build and run with Docker:
```bash
docker build -t rubiks-solver-api .
docker run -p 8000:8000 rubiks-solver-api
```

### Railway
Deploy to Railway:
```bash
railway link
railway up
```

### Render
Push to GitHub and connect Render to auto-deploy.

## 📊 Performance

- Image processing: ~100-200ms per image
- CNN inference: ~50-100ms per image
- Cube solving: ~10-50ms (depends on scramble complexity)

Total pipeline: ~500ms - 1.5s per complete solve

## 🐛 Common Issues

1. **CORS Error**: Update `CORS_ORIGINS` in config.py
2. **Model not found**: Run ML training script first
3. **Out of memory**: Reduce batch size or image size in config

## 📖 API Documentation

Interactive docs available at: `http://localhost:8000/docs`
