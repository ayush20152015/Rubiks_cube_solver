# Setup Guide - Rubik's Cube Solver

Complete step-by-step guide to set up and run the entire project locally.

## Prerequisites

- **Node.js & npm**: [Download Node.js 18+](https://nodejs.org/)
- **Python**: [Download Python 3.10+](https://www.python.org/)
- **Git**: [Download Git](https://git-scm.com/)
- **Docker** (optional): For containerized deployment

Verify installations:
```bash
node --version    # v18+
npm --version     # 8+
python --version  # 3.10+
git --version     # 2+
```

## Step 1: Clone Repository

```bash
git clone https://github.com/ayush20152015/Rubiks_cube_solver.git
cd Rubiks_cube_solver
git checkout visual_work
```

## Step 2: Environment Configuration

Copy environment template:
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```env
VITE_API_URL=http://localhost:8000
PYTHONUNBUFFERED=1
DEBUG=False
```

## Step 3: Frontend Setup

### Install Dependencies
```bash
cd frontend
npm install
cd ..
```

This installs:
- React 18
- Vite
- TypeScript
- Axios
- Development tools

### Verify Frontend Build
```bash
cd frontend
npm run build
cd ..
```

This creates production build in `frontend/dist/`.

## Step 4: Backend Setup

### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
cd ..
```

This installs:
- FastAPI
- Uvicorn
- OpenCV
- TensorFlow
- Pydantic
- Python-dotenv
- CORS support

### Verify Backend
```bash
cd backend
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import tensorflow; print('✓ TensorFlow installed')"
python -c "import cv2; print('✓ OpenCV installed')"
cd ..
```

## Step 5: ML Setup (Optional)

### Install ML Dependencies
```bash
cd ml
pip install -r requirements.txt
cd ..
```

This installs model training requirements.

### Train Model (Recommended for MVP)
```bash
cd ml
python train.py
cd ..
```

This:
- Generates synthetic training data
- Trains CNN model
- Saves to `models/face_classifier.h5`
- Takes ~2-5 minutes on CPU

## Step 6: Run Locally

### In Terminal 1 - Backend
```bash
cd backend
python main.py
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### In Terminal 2 - Frontend
```bash
cd frontend
npm run dev
```

Expected output:
```
  VITE v5.0.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
```

### Open Browser
Navigate to: `http://localhost:5173`

## Step 7: Test the App

1. **Navigate to Upload Section**
   - Click "Step 1: Upload Cube Faces"

2. **Upload Sample Images**
   - For each of 6 faces (UP, FRONT, RIGHT, BACK, LEFT, DOWN)
   - Click on the face card
   - Select an image (can be any image for MVP testing)
   - Wait for upload confirmation (green checkmark)

3. **Solve Cube**
   - Once all 6 faces uploaded, click "Solve Cube"
   - Wait for processing (~1-2 seconds)

4. **View Solution**
   - Moves displayed as sequence
   - Individual move badges shown
   - Final cube state grid displayed

## Directory Verification

After setup, your structure should look like:
```
Rubiks_cube_solver/
├── frontend/
│   ├── src/
│   ├── node_modules/  ← Created by npm install
│   ├── package.json
│   └── ...
├── backend/
│   ├── services/
│   ├── routes/
│   ├── main.py
│   └── ...
├── ml/
│   ├── train.py
│   ├── model.py
│   └── ...
├── models/
│   └── face_classifier.h5  ← Created by ml/train.py
├── .env
├── .github/
└── ...
```

## Troubleshooting

### Issue: "npm: command not found"
**Solution:** Install Node.js from https://nodejs.org/

### Issue: "python: command not found"
**Solution:** Install Python from https://www.python.org/

### Issue: Port 8000 already in use
**Solution:** Kill the process or use different port:
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows (PowerShell)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

### Issue: Port 5173 already in use
**Solution:** Vite will automatically use next available port

### Issue: CORS error in browser
**Solution:** 
1. Check backend CORS config in `backend/config.py`
2. Ensure your frontend URL is in `CORS_ORIGINS`
3. Restart backend after changing config

### Issue: Model not found error
**Solution:** Train the model:
```bash
cd ml
python train.py
```

### Issue: "ModuleNotFoundError: No module named 'tensorflow'"
**Solution:**
```bash
cd backend
pip install --upgrade pip
pip install -r requirements.txt
```

### Issue: Frontend can't connect to backend
**Solution:** 
1. Verify backend is running on `http://localhost:8000`
2. Check `VITE_API_URL` in `frontend/src/api/client.ts`
3. Check browser console for specific error

## Advanced Configuration

### Custom Backend Port
Edit `backend/main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)  # Change here
```

### Custom Frontend Port
Edit `frontend/vite.config.ts`:
```typescript
export default defineConfig({
  server: {
    port: 3000,  // Change here
  }
})
```

### Proxy Configuration
For production, use a reverse proxy (Nginx):
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://frontend:5173;
    }

    location /api/ {
        proxy_pass http://backend:8000/;
    }
}
```

## Docker Setup (Optional)

### Build and Run with Docker Compose
```bash
docker-compose up --build
```

This runs:
- Frontend on port 5173
- Backend on port 8000

### Individual Docker Builds

**Frontend:**
```bash
cd frontend
docker build -t rubiks-solver-ui .
docker run -p 5173:5173 rubiks-solver-ui
```

**Backend:**
```bash
cd backend
docker build -t rubiks-solver-api .
docker run -p 8000:8000 -v $(pwd)/models:/app/models rubiks-solver-api
```

## Development Workflow

### Making Changes

1. **Frontend Changes**
   - Edit files in `frontend/src/`
   - Vite auto-reloads browser
   - Run `npm run build` before deploying

2. **Backend Changes**
   - Edit files in `backend/`
   - Server needs manual restart: Ctrl+C, then `python main.py`
   - Or use auto-reload: `pip install watchdog[watchmedo]` and run with watchdog

3. **ML Changes**
   - Retrain model: `cd ml && python train.py`
   - Restart backend to load new model

### Running Tests

**Backend Tests:**
```bash
cd backend
pip install pytest pytest-cov
pytest
```

**Frontend Build Test:**
```bash
cd frontend
npm run build
```

## Deployment Guide

### Frontend Deployment (Vercel)

1. **Create Vercel Account**
   - Go to https://vercel.com
   - Sign up with GitHub

2. **Import Project**
   - Click "New Project"
   - Select your GitHub repo
   - Configure build settings:
     - Root Directory: `frontend`
     - Build Command: `npm run build`
     - Output Directory: `dist`

3. **Environment Variables**
   - Add `VITE_API_URL` pointing to deployed backend

4. **Deploy**
   - Click "Deploy"

### Backend Deployment (Railway)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Service**
   - Connect your GitHub repo
   - Select Python
   - Configure environment:
     - Working directory: `backend`
     - Start command: `pip install -r requirements.txt && python main.py`

3. **Environment Variables**
   - Add all settings from `.env`

4. **Deploy**
   - Click "Deploy"

### Database & Storage

For future enhancement with persistent storage:
- **Database**: PostgreSQL on Railway/Render
- **File Storage**: AWS S3 / Firebase Storage
- **Model Storage**: Cloud bucket or CDN

## Performance Monitoring

### Local Monitoring

Monitor backend performance:
```bash
cd backend
pip install prometheus-client
# Add Prometheus middleware to FastAPI app
```

### Production Monitoring

Use services:
- **Vercel Analytics** for frontend
- **Sentry** for error tracking
- **New Relic** for backend monitoring

## Next Steps

1. ✅ Complete local setup
2. ✅ Test the application
3. ✅ Train custom ML model with Kaggle dataset
4. 🔄 Integrate C++ solver (optional optimization)
5. 🔄 Deploy to production
6. 🔄 Collect user feedback
7. 🔄 Iterate and improve

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TensorFlow Guide](https://www.tensorflow.org/)
- [Vite Documentation](https://vitejs.dev/)
- [Vercel Docs](https://vercel.com/docs)

## Support

For issues or questions:
1. Check troubleshooting section above
2. Review component README files
3. Open GitHub issue with details
4. Check logs in terminal for error messages

---

**Happy solving! 🎲**
