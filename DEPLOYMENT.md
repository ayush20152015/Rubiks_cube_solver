# 🚀 Deployment Guide - Vercel + GitHub + Railway

Complete step-by-step guide to deploy your Rubik's Cube Solver to production.

## Prerequisites

- GitHub account (already set up) ✅
- Vercel account (free tier available at vercel.com)
- Railway account (for backend, free tier available at railway.app)

---

## Part 1: Frontend Deployment (Vercel)

### Step 1: Create Vercel Account & Connect GitHub

1. Go to **https://vercel.com**
2. Click "Sign Up"
3. Select "Continue with GitHub"
4. Authorize Vercel to access your GitHub account
5. Verify your email

### Step 2: Import Project to Vercel

1. Go to **https://vercel.com/new**
2. Select "Import Git Repository"
3. Search for `Rubiks_cube_solver`
4. Click "Import"

### Step 3: Configure Project Settings

**In the import dialog, set:**

| Setting | Value |
|---------|-------|
| **Project Name** | `rubiks-cube-solver` (or your choice) |
| **Root Directory** | `frontend/` |
| **Framework** | `Vite` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

### Step 4: Add Environment Variables

1. Click "Environment Variables"
2. Add these variables:

```
VITE_API_URL=https://your-backend-url.com
```

(We'll set the backend URL after deploying the backend)

### Step 5: Deploy

1. Click "Deploy"
2. Wait for build to complete (~2-3 minutes)
3. You'll get a URL like: `https://rubiks-cube-solver.vercel.app`

**✅ Frontend is now live!**

---

## Part 2: Backend Deployment (Railway)

### Step 1: Create Railway Account

1. Go to **https://railway.app**
2. Click "Start a New Project"
3. Sign up with GitHub
4. Authorize Railway to access your account

### Step 2: Deploy from Repository

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Select your `Rubiks_cube_solver` repo
4. Confirm

### Step 3: Configure Railway Service

1. Railway will auto-detect Python project
2. Wait for build to complete
3. Once deployed, you'll get a public URL

### Step 4: Add Environment Variables

1. Go to your Railway project
2. Click "Variables"
3. Add these:

```
PYTHONUNBUFFERED=1
DEBUG=False
CORS_ORIGINS=["https://rubiks-cube-solver.vercel.app", "http://localhost:5173"]
```

4. Click "Save"

### Step 5: Get Backend URL

1. Go to "Deployments"
2. Click your service
3. Copy the public URL (e.g., `https://rubiks-cube-solver-api-prod.up.railway.app`)

**✅ Backend is now live!**

---

## Part 3: Update Frontend with Backend URL

### Update Vercel Environment Variables

1. Go to your Vercel project settings
2. Click "Environment Variables"
3. Update `VITE_API_URL` with your Railway backend URL:

```
VITE_API_URL=https://rubiks-cube-solver-api-prod.up.railway.app
```

4. The deployment will automatically redeploy with the new env var

---

## Verify Deployment

### Check Frontend

- Visit `https://rubiks-cube-solver.vercel.app`
- You should see the Rubik's Cube Solver UI
- Try uploading an image (should connect to backend)

### Check Backend

- Visit `https://your-backend-url.com/docs`
- You should see FastAPI Swagger documentation
- All endpoints should be available

### Check Health

```bash
# Check frontend
curl https://rubiks-cube-solver.vercel.app

# Check backend API
curl https://your-backend-url.com/health
```

---

## GitHub Actions CI/CD Integration

Your workflows are already configured! Here's what happens:

### On Every Push to `main`:
1. ✅ Backend tests run (pytest)
2. ✅ Frontend builds (Vite)
3. ✅ ML model training (optional)
4. ✅ Automatic deployment to Vercel + Railway

### On Pull Requests:
1. ✅ Backend linting + tests
2. ✅ Frontend build validation
3. ✅ Results shown in PR checks

**To enable automatic deployment:**

1. Go to your Vercel project settings
2. Enable "Automatically deploy when GitHub branch is updated"
3. Same for Railway

---

## Troubleshooting

### "CORS error" in browser console

**Solution:**
```
1. Check backend CORS_ORIGINS includes your Vercel URL
2. Backend variable should be:
   CORS_ORIGINS=["https://your-vercel-url.com", "http://localhost:5173"]
3. Restart Railway service
```

### "Cannot reach backend" error

**Solution:**
1. Verify backend URL in Vercel env vars
2. Ensure `VITE_API_URL` is correct
3. Check Railway service is running (green status)
4. Verify CORS settings in backend

### Build fails on Vercel

**Solution:**
1. Check build logs in Vercel dashboard
2. Ensure `frontend/package.json` exists
3. Run `npm install && npm run build` locally to test
4. Check for syntax errors in React code

### Build fails on Railway

**Solution:**
1. Check build logs in Railway
2. Ensure Python version is 3.10+ (set in railway.json)
3. Run `pip install -r requirements.txt` locally to verify
4. Check for Python syntax errors

### Models directory missing

**Solution:**
1. Train ML model locally: `cd ml && python train.py`
2. Commit `models/face_classifier.h5` to repo
3. Or update backend to use a cloud-hosted model

---

## Production Optimizations

### Frontend (Vercel)

Already optimized! Vercel provides:
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Auto-scaling
- ✅ Free SSL certificates
- ✅ Environment-based builds

### Backend (Railway)

To optimize:

1. **Upgrade Plan**
   - Free tier: 500 hours/month
   - Paid: Unlimited with auto-scaling

2. **Enable Auto-scaling**
   - Railway dashboard → Project settings
   - Set max replicas (for load balancing)

3. **Database Connection**
   - Add PostgreSQL plugin
   - Update backend config for persistence

4. **Monitoring**
   - Enable Railway monitoring
   - Set up alerts

---

## Monitoring & Debugging

### Vercel Monitoring

1. Go to Vercel dashboard
2. Click your project
3. View analytics:
   - Response times
   - Error rates
   - Bandwidth usage

### Railway Monitoring

1. Go to Railway dashboard
2. View logs in real-time
3. Monitor CPU, memory, disk usage

### Enable Error Tracking

Add Sentry for error reporting:

```python
# In backend/main.py
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

---

## GitHub Actions Secrets Setup

Configure these in GitHub for auto-deployment:

1. Go to GitHub repo → Settings → Secrets and variables → Actions

2. Add these secrets:
```
VERCEL_TOKEN         # From https://vercel.com/account/tokens
VERCEL_ORG_ID        # From Vercel project settings
VERCEL_PROJECT_ID    # From Vercel project settings
RAILWAY_TOKEN        # From Railway project settings
```

3. Update `.github/workflows/deploy.yml` with your tokens

---

## Custom Domain Setup

### Vercel Custom Domain

1. Go to Vercel project settings
2. Click "Domains"
3. Enter your domain (e.g., `cube-solver.com`)
4. Add DNS records (shown by Vercel)
5. Wait for DNS propagation (~24 hours)

### Railway Custom Domain

1. Go to Railway project settings
2. Add domain in Environment tab
3. Update DNS records
4. Wait for propagation

---

## Scaling for Production

### When Traffic Grows:

**Frontend:**
- Vercel handles auto-scaling automatically
- Use caching headers for images
- Consider Cloudflare for additional CDN

**Backend:**
- Upgrade Railway plan
- Enable auto-scaling
- Add PostgreSQL for session storage
- Implement Redis for caching
- Use Docker multi-stage builds for efficiency

### Database (Future)

When you need persistence:
1. Railway has integrated PostgreSQL
2. Create database plugin
3. Update backend `config.py`
4. Initialize schema

---

## Rollback Procedures

### Vercel Rollback

1. Go to Deployments
2. Find previous deployment
3. Click "Rollback"
4. Confirm

### Railway Rollback

1. Go to Deployments
2. Select previous version
3. Click "Reactivate"

---

## Next Steps

1. ✅ Deploy frontend to Vercel
2. ✅ Deploy backend to Railway
3. ✅ Connect frontend to backend
4. ✅ Test end-to-end
5. 🔄 Set up custom domain
6. 🔄 Enable monitoring
7. 🔄 Configure auto-scaling
8. 🔄 Add database for production data

---

## Links & Resources

| Resource | URL |
|----------|-----|
| Vercel | https://vercel.com |
| Railway | https://railway.app |
| GitHub | https://github.com |
| Vercel Docs | https://vercel.com/docs |
| Railway Docs | https://docs.railway.app |
| FastAPI Docs | https://fastapi.tiangolo.com |
| React Docs | https://react.dev |

---

## Support & Questions

- **Vercel Support**: https://vercel.com/support
- **Railway Support**: https://railway.app/support
- **GitHub Support**: https://support.github.com

---

**You're all set! Your Rubik's Cube Solver is now deployed to production! 🎲✨**
