# 🎲 Rubik's Cube Solver - ML-Powered Pipeline

An end-to-end pipeline that solves a Rubik's Cube from 6 phone-captured face images using CNN-based color detection and the IDA* search algorithm.

## ✨ Features

- 📷 **6-Face Image Upload**: Upload images of each cube face (supports arbitrary lighting/backgrounds)
- 🧠 **CNN Color Detection**: Detects 3×3 color grid for each face (W, R, G, B, O, Y)
- 🔧 **Cube State Reconstruction**: Builds internal cube state from detected colors
- ⚡ **IDA* Solver**: Generates optimal solution move sequence
- 🎨 **Interactive UI**: React-based web interface for intuitive interaction
- 🚀 **Deployment-Ready**: FastAPI backend + Vercel-hosted frontend
- 🔄 **CI/CD Pipeline**: GitHub Actions for automated testing and deployment

## 🏗️ Project Structure

```
.
├── frontend/                    # React + Vite + TypeScript
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── api/                 # API client
│   │   ├── types/               # TypeScript types
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── tsconfig.json
│
├── backend/                     # Python FastAPI
│   ├── routes/                  # API endpoints
│   ├── services/                # Business logic
│   │   ├── image_processor.py   # Image preprocessing
│   │   ├── model_inference.py   # CNN inference
│   │   └── cube_solver.py       # Cube solving logic
│   ├── main.py                  # FastAPI app
│   ├── config.py                # Configuration
│   └── requirements.txt
│
├── ml/                          # ML Training & Inference
│   ├── model.py                 # CNN architecture
│   ├── data_loader.py           # Dataset loading
│   ├── train.py                 # Training script
│   ├── inference.py             # Inference utilities
│   └── requirements.txt
│
├── models/                      # Trained models (generated during training)
│   └── face_classifier.h5       # Trained CNN model
│
├── .github/workflows/           # GitHub Actions CI/CD
│   ├── backend-tests.yml
│   ├── frontend-build.yml
│   ├── deploy.yml
│   └── ml-training.yml
│
└── Model/                       # Original C++ Rubik's Cube Solver
    └── (existing solver code)
```

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.10+
- pip

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/ayush20152015/Rubiks_cube_solver.git
   cd Rubiks_cube_solver
   ```

2. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Install Frontend Dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

4. **Install Backend Dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

5. **Install ML Dependencies** (optional, for training)
   ```bash
   cd ml
   pip install -r requirements.txt
   cd ..
   ```

### Running Locally

**Terminal 1 - Backend API**
```bash
cd backend
python main.py
```

The backend runs on `http://localhost:8000`

**Terminal 2 - Frontend Dev Server**
```bash
cd frontend
npm run dev
```

The frontend runs on `http://localhost:5173`

Open your browser to `http://localhost:5173` and start solving cubes!

### API Documentation

Once the backend is running, view API docs at: `http://localhost:8000/docs`

## 📚 Detailed Documentation

- [Frontend README](./frontend/README.md) - React app setup and component guide
- [Backend README](./backend/README.md) - FastAPI setup and API endpoints
- [ML README](./ml/README.md) - Model training and inference guide
- [SETUP.md](./SETUP.md) - Detailed setup and deployment instructions

## 🤖 CNN Model Training

To train the color classification model:

```bash
cd ml
python train.py
```

This will:
1. Load the Rubik's Cube face dataset (or generate synthetic data for testing)
2. Train a CNN model to classify 3×3 color grids
3. Save the trained model to `../models/face_classifier.h5`

### Using Real Data

Download the [Kaggle Rubik's Cube Face Dataset](https://www.kaggle.com/datasets/aryan7004/rubiks-cube-face-dataset/) and update the data loader path in `ml/train.py`.

## 🧩 Pipeline Stages

### Stage 1: Image Upload
- User uploads 6 images (one per face)
- UI shows upload progress and preview thumbnails
- Each image is sent to backend with face_id

### Stage 2: Color Detection
- Backend receives image
- Image preprocessing: resize, normalize, augment
- CNN model infers 3×3 color grid
- Colors returned as matrix: `[['W', 'R', 'G'], ...]`

### Stage 3: Cube Reconstruction
- All 6 face grids are stitched into internal cube representation
- Validation ensures valid cube state (9 of each color)

### Stage 4: Solving
- IDA* algorithm generates optimal move sequence
- Moves returned in standard notation: `R U R' U' ...`

### Stage 5: Display Solution
- Frontend shows:
  - Number of moves required
  - Move sequence as badges
  - Final solved cube state visualization

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Build
```bash
cd frontend
npm run build
```

### GitHub Actions
Tests run automatically on push to `main` and `visual_work` branches.

## 🚢 Deployment

### Frontend (Vercel)
```bash
cd frontend
npm run build
# Deploy to Vercel using Vercel CLI or GitHub integration
vercel deploy
```

### Backend (Railway/Render)
Create a deployment configuration for your preferred platform:
- Railway: Add `railway.json` or use Railway CLI
- Render: Add `render.yaml`
- Heroku: Add `Procfile`

Configure GitHub secrets:
- `VERCEL_TOKEN`
- `VERCEL_ORG_ID`
- `VERCEL_PROJECT_ID`
- `RAILWAY_TOKEN` (or equivalent for your platform)

## 📡 API Endpoints

### Core Endpoints

- `POST /api/v1/cube/upload-face` - Upload a face image
- `POST /api/v1/cube/solve` - Solve the cube
- `POST /api/v1/cube/reset` - Reset cube state
- `GET /api/v1/cube/state` - Get current cube state
- `GET /api/v1/cube/health` - Health check

See [Backend README](./backend/README.md) for detailed endpoint documentation.

## 🎨 Technology Stack

### Frontend
- React 18
- TypeScript
- Vite
- Axios

### Backend
- FastAPI
- Python 3.10+
- OpenCV
- TensorFlow/Keras

### ML
- TensorFlow
- Keras
- NumPy
- scikit-learn

### DevOps
- GitHub Actions (CI/CD)
- Docker
- Vercel (Frontend)
- Railway/Render (Backend)

## 🐛 Troubleshooting

### CORS Errors
Make sure the backend CORS settings include your frontend URL in `backend/config.py`:
```python
CORS_ORIGINS: list[str] = ["http://localhost:5173", "http://your-vercel-url.com"]
```

### Model Not Loading
Ensure `models/face_classifier.h5` exists or train the model:
```bash
cd ml && python train.py
```

### Port Already in Use
- Backend: Change port in `backend/main.py`
- Frontend: Change port in `frontend/vite.config.ts`

## 📝 TODOs & Roadmap

- [ ] Integrate C++ solver via Python bindings for faster solving
- [ ] Add 3D cube visualization
- [ ] Support for different cube sizes (2×2, 4×4, etc.)
- [ ] Mobile app version
- [ ] Real-time solution preview
- [ ] Leaderboard for fastest solves
- [ ] Multi-language support

## 📄 License

This project is open source. See LICENSE for details.

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

Ayush - [GitHub](https://github.com/ayush20152015)

## 🙏 Acknowledgments

- Original Rubik's Cube Solver (C++)
- [Kaggle Rubik's Cube Face Dataset](https://www.kaggle.com/datasets/aryan7004/rubiks-cube-face-dataset/)
- IDA* Algorithm references

---

**Made with ❤️ for cube enthusiasts and ML learners**
