# Architecture & Design Overview

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER (Phone/Browser)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
        ┌────────────────────────────┐
        │   React Web UI (Vercel)    │
        │  - 6 Face Image Upload     │
        │  - Solution Display        │
        │  - Cube Visualization      │
        └────────────┬───────────────┘
                     │ HTTP/Axios
                     ▼
        ┌────────────────────────────┐
        │  FastAPI Backend           │
        │  (Railway/Render)          │
        │  - Image Upload Handler    │
        │  - Color Detection Service │
        │  - Cube Solver Service     │
        │  - Solution Generator      │
        └────────────┬───────────────┘
                     │
        ┌────────────┴──────────────┐
        │                           │
        ▼                           ▼
   ┌─────────────┐         ┌─────────────────┐
   │ CNN Model   │         │ Cube Solver     │
   │ (TensorFlow)│         │ (C++/Python)    │
   │ - Load H5   │         │ - State Mgmt    │
   │ - Inference │         │ - Solve Logic   │
   └─────────────┘         │ - Move Sequence │
                           └─────────────────┘
```

## Component Breakdown

### 1. Frontend (React + TypeScript + Vite)

**Entry Point:** `frontend/src/App.tsx`

**Components:**
- `ImageUpload.tsx` - Drag-drop or click-to-upload interface for cube faces
- `SolutionDisplay.tsx` - Shows moves and final cube state visualization

**Key Features:**
- Responsive grid layout (6 face cards)
- Real-time upload progress
- Move sequence display with badges
- 3×3 color grid visualization

**Technologies:**
- React 18 (UI framework)
- TypeScript (type safety)
- Vite (fast bundler)
- Axios (HTTP client)
- CSS modules (styling)

### 2. Backend (FastAPI + Python)

**Entry Point:** `backend/main.py`

**Services:**
- `ImageProcessor` - Image loading, resizing, normalization
- `ModelInference` - CNN inference for color detection
- `CubeSolver` - Cube state management and solving

**Routes:** `backend/routes/cube.py`
- `POST /api/v1/cube/upload-face` - Receive image + face_id
- `POST /api/v1/cube/solve` - Trigger solving
- `GET /api/v1/cube/state` - Current cube state
- `POST /api/v1/cube/reset` - Reset to default

**Key Features:**
- CORS-enabled for cross-origin requests
- Multipart file upload support
- Asynchronous request handling
- Interactive Swagger docs at `/docs`

**Technologies:**
- FastAPI (web framework)
- Uvicorn (ASGI server)
- OpenCV (image processing)
- TensorFlow (model inference)
- Pydantic (data validation)

### 3. ML Pipeline (CNN Model Training)

**Entry Point:** `ml/train.py`

**Components:**
- `CubeColorCNN` - Neural network architecture (6-class classifier)
- `CubeDataLoader` - Loads Kaggle dataset or generates synthetic data
- `CubeInference` - Loads model and runs predictions

**Model Details:**
- Input: 224×224×3 RGB images
- Output: 6 color classes (W, R, G, B, O, Y)
- Architecture: 3 conv blocks + dense layers
- Training: Adam optimizer, categorical crossentropy loss

**Key Features:**
- Batch normalization
- Dropout regularization
- Early stopping (avoid overfitting)
- Learning rate scheduling
- Save/load functionality

**Technologies:**
- TensorFlow/Keras
- scikit-learn (train/test split)
- PIL (image loading)
- NumPy (numerical ops)

### 4. Original C++ Solver (Optional Integration)

**Location:** `Model/`, `Solver/`, `PatternDatabases/`

**Features:**
- IDA* search algorithm
- Corner pattern database (heuristic)
- Multiple cube representations
- Fast move generation

**Integration Potential:**
- Compile C++ to Python bindings (ctypes, pybind11)
- Call from Python backend for faster solving
- Use existing database for heuristics

## Data Flow

### Single Solve Request Flow

```
1. User Upload
   └─> Browser: Select image + face_id
       └─> POST /api/v1/cube/upload-face
           └─> FastAPI receives multipart file

2. Image Processing
   └─> ImageProcessor.preprocess_image()
       └─> Load from bytes → Resize to 224×224 → Normalize [-1, 1]

3. Color Detection
   └─> CNN Model.predict()
       └─> Model inference on preprocessed image
           └─> Returns probabilities for 6 colors
               └─> Extract 3×3 color grid

4. State Update
   └─> CubeSolver.set_face(face_id, colors)
       └─> Update internal cube representation

5. User Requests Solution
   └─> POST /api/v1/cube/solve
       └─> CubeSolver.is_valid_cube() - Validate
           └─> CubeSolver.solve() - Generate moves
               └─> Return [moves, final_state]

6. Display Solution
   └─> Browser receives response
       └─> Display move sequence + colored cube state
           └─> User sees complete solution
```

## State Management

### Cube State Representation

```python
cube_state = {
    'U': [['W', 'W', 'W'], ['W', 'W', 'W'], ['W', 'W', 'W']],  # UP (White)
    'D': [['Y', 'Y', 'Y'], ['Y', 'Y', 'Y'], ['Y', 'Y', 'Y']],  # DOWN (Yellow)
    'F': [['R', 'R', 'R'], ['R', 'R', 'R'], ['R', 'R', 'R']],  # FRONT (Red)
    'B': [['O', 'O', 'O'], ['O', 'O', 'O'], ['O', 'O', 'O']],  # BACK (Orange)
    'L': [['G', 'G', 'G'], ['G', 'G', 'G'], ['G', 'G', 'G']],  # LEFT (Green)
    'R': [['B', 'B', 'B'], ['B', 'B', 'B'], ['B', 'B', 'B']],  # RIGHT (Blue)
}
```

**Validation Rules:**
- Each color appears exactly 9 times
- Only valid colors (W, R, G, B, O, Y) allowed
- Stickers positions must be valid

## API Contract

### Upload Face Request
```json
POST /api/v1/cube/upload-face
Content-Type: multipart/form-data

{
  "image": <binary>,
  "face_id": 0
}
```

### Upload Face Response
```json
{
  "face_id": 0,
  "face_name": "UP",
  "colors": [["W", "W", "W"], ["W", "R", "W"], ["W", "W", "W"]],
  "success": true
}
```

### Solve Request
```json
POST /api/v1/cube/solve
{}
```

### Solve Response
```json
{
  "moves": ["R", "U", "R'", "U'", "R", "U2", "R'"],
  "cube_state": { ... },
  "success": true
}
```

## Deployment Architecture

### Development
```
Local Machine
├─ Frontend: npm run dev (port 5173)
├─ Backend: python main.py (port 8000)
└─ ML: Training scripts
```

### Production
```
CDN + Vercel
├─ Frontend: React SPA (built dist/)
│   └─ Served on vercel.com domain
│
Cloud Platform (Railway/Render/Heroku)
└─ Backend: FastAPI service
    ├─ Database: (future)
    └─ Models: /models/ directory
```

## Performance Targets

| Operation | Target | Actual (Dev) |
|-----------|--------|-------------|
| Image Upload | <1s | ~500ms |
| Color Detection | <500ms | ~200ms |
| Cube Validation | <100ms | ~50ms |
| Solving | <1s | ~100-500ms |
| Total Pipeline | <3s | ~1-2s |

## Scalability Considerations

### Current MVP Limits
- Single-threaded request handling
- No request queuing
- Models loaded in memory
- No caching

### Future Improvements
- Async request processing (FastAPI already supports)
- Redis caching for solved states
- Load balancing for multiple instances
- Model optimization (quantization, TF Lite)
- Database for storing solve history

## Security Considerations

### Current MVP
- CORS restricted to localhost
- No authentication
- File size limit: 10MB
- Basic input validation

### Production Checklist
- [ ] Enable HTTPS/SSL
- [ ] Add authentication (JWT/OAuth)
- [ ] Rate limiting per IP
- [ ] Input sanitization
- [ ] Logging and monitoring
- [ ] Error message scrubbing
- [ ] CORS whitelist for production domains

## Testing Strategy

### Unit Tests
- Cube state validation
- Color detection accuracy
- API endpoint contracts

### Integration Tests
- Full upload → solve pipeline
- Multiple concurrent requests
- Error handling

### E2E Tests
- Browser-based testing
- Actual image uploads
- Complete user flow

## Monitoring & Logging

### Logging
- Backend: FastAPI request logs + custom service logs
- Frontend: Browser console + error tracking (Sentry)

### Metrics
- API response times
- Model inference time
- Error rates
- User activity

### Alerts
- Service downtime
- High error rates
- Slow response times
- Model failures

---

**This architecture is designed for MVP with production-readiness in mind.**
