# 🚀 DEPLOYMENT GUIDE

## 📦 Pre-Deployment Checklist

- [ ] All dependencies installed
- [ ] ML model trained (model.pkl exists)
- [ ] Backend tested locally
- [ ] Frontend tested locally
- [ ] API endpoints working
- [ ] CORS configured properly

## 🌐 OPTION 1: Deploy Backend to Render

### Step 1: Prepare Backend

1. Create `render.yaml` in project root:

```yaml
services:
  - type: web
    name: nutricare-backend
    env: python
    buildCommand: "cd backend && pip install -r requirements.txt"
    startCommand: "cd backend && python app.py"
    envVars:
      - key: PORT
        value: 5000
```

2. Ensure `requirements.txt` has all dependencies:
```
flask
firebase-admin
pandas
numpy
scikit-learn
flask-cors
joblib
openpyxl
```

### Step 2: Deploy to Render

1. Go to [render.com](https://render.com)
2. Sign up / Login
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure:
   - Name: `nutricare-backend`
   - Environment: `Python 3`
   - Build Command: `cd backend && pip install -r requirements.txt`
   - Start Command: `cd backend && python app.py`
6. Click "Create Web Service"
7. Wait for deployment (5-10 minutes)
8. Copy your backend URL: `https://nutricare-backend.onrender.com`

### Step 3: Update Frontend

In `frontend/dashboard.js`, update:

```javascript
const API_BASE_URL = "https://nutricare-backend.onrender.com";
```

## 🌐 OPTION 2: Deploy Backend to Heroku

### Step 1: Create Procfile

Create `Procfile` in backend folder:
```
web: python app.py
```

### Step 2: Create runtime.txt

Create `runtime.txt` in backend folder:
```
python-3.11.0
```

### Step 3: Deploy

```bash
cd backend
heroku login
heroku create nutricare-backend
git init
git add .
git commit -m "Initial commit"
git push heroku main
```

### Step 4: Get URL

```bash
heroku open
```

Copy the URL and update `dashboard.js`

## 🌐 Deploy Frontend to Netlify

### Step 1: Prepare Frontend

1. Update `API_BASE_URL` in `dashboard.js` with your backend URL
2. Test locally to ensure it works

### Step 2: Deploy to Netlify

**Option A: Drag & Drop**
1. Go to [netlify.com](https://netlify.com)
2. Sign up / Login
3. Drag the `frontend` folder to Netlify
4. Done! Get your URL

**Option B: GitHub**
1. Push code to GitHub
2. Connect Netlify to GitHub
3. Select repository
4. Set publish directory: `frontend`
5. Deploy

### Step 3: Custom Domain (Optional)

1. Go to Domain Settings
2. Add custom domain
3. Update DNS records

## 🌐 Deploy Frontend to Vercel

### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

### Step 2: Deploy

```bash
cd frontend
vercel
```

Follow prompts and get your URL

## 🌐 Deploy Frontend to GitHub Pages

### Step 1: Create Repository

1. Create new GitHub repository
2. Push your code

### Step 2: Enable GitHub Pages

1. Go to Settings → Pages
2. Source: `main` branch
3. Folder: `/frontend`
4. Save

### Step 3: Access

Your site: `https://yourusername.github.io/nutricare-ai/`

## 🔐 Environment Variables

### Backend Environment Variables

For production, set these on Render/Heroku:

```
PORT=5000
GOOGLE_APPLICATION_CREDENTIALS=/path/to/firebase-key.json
FLASK_ENV=production
```

### Firebase Setup (Optional)

1. Create Firebase project
2. Generate service account key
3. Upload to Render/Heroku as secret file
4. Set environment variable path

## 🧪 Testing Production

### Test Backend

```bash
curl https://your-backend-url.com/
```

Expected response:
```json
{
  "status": "running",
  "service": "Maternal Nutrition AI Backend"
}
```

### Test Analysis Endpoint

```bash
curl -X POST https://your-backend-url.com/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "age": 28,
    "systolicbp": 120,
    "diastolicbp": 80,
    "bs": 7.5,
    "bodytemp": 98.6,
    "heartrate": 75
  }'
```

### Test Frontend

1. Open your frontend URL
2. Enter health data
3. Click "Analyze Health"
4. Verify all features work

## 📊 Monitoring

### Render
- View logs in Render dashboard
- Monitor uptime
- Check resource usage

### Heroku
```bash
heroku logs --tail
```

### Netlify
- View deploy logs
- Check analytics
- Monitor bandwidth

## 🔄 Updates & Redeployment

### Backend Updates

**Render:**
- Push to GitHub
- Auto-deploys on commit

**Heroku:**
```bash
git add .
git commit -m "Update"
git push heroku main
```

### Frontend Updates

**Netlify:**
- Push to GitHub (auto-deploy)
- Or drag & drop new files

**Vercel:**
```bash
vercel --prod
```

## 🐛 Troubleshooting

### Backend Issues

**Problem:** 500 Internal Server Error
- Check logs for errors
- Verify all dependencies installed
- Check ML model files exist

**Problem:** CORS Error
- Verify CORS is enabled in app.py
- Check API_BASE_URL in frontend
- Ensure OPTIONS method handled

**Problem:** Model not found
- Upload model.pkl to deployment
- Or train model on server

### Frontend Issues

**Problem:** API not reachable
- Check backend URL is correct
- Verify backend is running
- Check CORS configuration

**Problem:** Chart not showing
- Verify Chart.js CDN loaded
- Check browser console for errors

## 📈 Performance Optimization

### Backend
- Enable caching
- Use production WSGI server (gunicorn)
- Optimize ML model loading

### Frontend
- Minify CSS/JS
- Enable CDN
- Optimize images
- Enable gzip compression

## 🔒 Security

### Backend
- Use HTTPS only
- Validate all inputs
- Sanitize user data
- Rate limiting
- Environment variables for secrets

### Frontend
- HTTPS only
- Input validation
- XSS protection
- CSP headers

## 💰 Cost Estimation

### Free Tier Options

**Render:**
- Free tier: 750 hours/month
- Sleeps after 15 min inactivity
- Good for demo/testing

**Heroku:**
- Free tier: 550 hours/month
- Sleeps after 30 min inactivity

**Netlify:**
- Free tier: 100GB bandwidth
- Unlimited sites

**Vercel:**
- Free tier: 100GB bandwidth
- Unlimited deployments

### Paid Options

**Render:** $7/month (always on)
**Heroku:** $7/month (hobby tier)
**Netlify:** $19/month (pro)
**Vercel:** $20/month (pro)

## 🎯 Recommended Setup

**For Demo/Testing:**
- Backend: Render (Free)
- Frontend: Netlify (Free)
- Total Cost: $0

**For Production:**
- Backend: Render ($7/month)
- Frontend: Netlify (Free)
- Total Cost: $7/month

## ✅ Post-Deployment

- [ ] Test all features
- [ ] Share URL with users
- [ ] Monitor logs
- [ ] Set up analytics
- [ ] Create backup plan
- [ ] Document API
- [ ] Set up monitoring alerts

---

**Your NutriCare AI is now live! 🎉**
