# Frontend - Rubik's Cube Solver UI

React + TypeScript web application for uploading cube faces and viewing solutions.

## 📋 Requirements

- Node.js 18+
- npm or yarn

## 🚀 Installation

```bash
npm install
```

## 🏃 Running the App

**Development:**
```bash
npm run dev
```

Starts dev server at `http://localhost:5173`

**Production Build:**
```bash
npm run build
```

Outputs optimized build to `dist/`

**Preview Production Build:**
```bash
npm run preview
```

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ImageUpload.tsx       # Image upload component
│   │   ├── ImageUpload.css
│   │   ├── SolutionDisplay.tsx   # Solution viewer
│   │   └── SolutionDisplay.css
│   │
│   ├── api/
│   │   └── client.ts             # Axios API client
│   │
│   ├── types/
│   │   └── index.ts              # TypeScript types
│   │
│   ├── App.tsx                   # Main app component
│   ├── App.css
│   └── main.tsx                  # Entry point
│
├── index.html                    # HTML template
├── vite.config.ts               # Vite configuration
├── tsconfig.json                # TypeScript config
└── package.json
```

## 🎨 Components

### ImageUpload
Handles uploading images for cube faces.

**Props:**
```typescript
interface Props {
  faceId: number;           // 0-5
  faceName: string;         // "UP (White)", etc.
  isUploaded: boolean;      // Upload status
  onUpload: (faceId: number, file: File) => void;
  disabled: boolean;        // Disable during processing
}
```

### SolutionDisplay
Shows solution moves and final cube state.

**Props:**
```typescript
interface Props {
  moves: string[];          // Move sequence
  cubeState: any;           // Final cube state
}
```

## 📡 API Integration

The `api/client.ts` module handles all backend communication:

```typescript
// Upload an image
await uploadFaceImage(file, faceId);

// Solve the cube
await solveCube();

// Get cube state
await getCubeState();

// Reset
await resetCube();
```

## 🔧 Configuration

### Backend URL
Set in environment or `vite.config.ts`:

```typescript
const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'
```

### Proxy Setup
Vite proxy is configured in `vite.config.ts` for development.

## 🎨 Styling

- CSS modules per component
- Responsive grid layout
- Gradient backgrounds
- Mobile-friendly design

## 📦 Build & Deploy

### Production Build
```bash
npm run build
```

### Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Deploy to GitHub Pages
```bash
npm run build
# Push dist/ to gh-pages branch
```

### Docker Deployment
```bash
docker build -t rubiks-solver-ui .
docker run -p 5173:5173 rubiks-solver-ui
```

## 🔐 Environment Variables

Create `.env.local`:

```
VITE_API_URL=http://localhost:8000
VITE_APP_TITLE=Rubik's Cube Solver
```

Or for production:

```
VITE_API_URL=https://your-api-url.com
```

## 🧪 Linting

```bash
npm run lint
```

## 🐛 Troubleshooting

1. **API connection failed**: Check `VITE_API_URL` in config
2. **CORS error**: Update backend `config.py` with frontend URL
3. **Build fails**: Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`

## 📱 Responsive Design

The app is responsive and works on:
- Desktop (1920px and above)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## ⚡ Performance

- Uses Vite for fast HMR
- Code splitting for smaller bundles
- Lazy loading of components
- Optimized images

## 🎯 Features

- ✅ 6-face image upload with preview
- ✅ Real-time upload status
- ✅ Solution display with move badges
- ✅ 3D cube state visualization
- ✅ Error handling and validation
- ✅ Dark mode ready
- ✅ Accessibility (WCAG)

## 📖 Development

### File Organization
- Components in `src/components/`
- API logic in `src/api/`
- Types in `src/types/`
- Styles co-located with components

### Code Style
- TypeScript strict mode enabled
- ESLint recommended rules
- Prettier formatting (when configured)

## 🚀 Performance Optimization

- React.StrictMode for dev checks
- Memoization where needed
- Conditional rendering
- Lazy loading of images

## 📄 License

See LICENSE in root directory
