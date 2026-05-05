# EDUPATH Deployment Guide

Deploying EDUPATH involves hosting two main components: the FastAPI Backend (with the ML model and SQLite database) and the React Frontend.

Here is the recommended approach to deploy this startup product to production for free or at a very low cost.

## 1. Backend Deployment (Render or Railway)
We recommend using Render.com or Railway.app for the backend because they easily support Python, FastAPI, and file persistence (required for your SQLite database and `.joblib` ML model).

**Steps for Render:**
1. Push your EDUPATH project to a GitHub repository.
2. Create an account on Render.com.
3. Create a **New Web Service** and connect your GitHub repository.
4. Configuration:
   - **Root Directory:** `backend`
   - **Environment:** `Python`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port 10000`
5. Environment Variables:
   - Add `SECRET_KEY` = `your-super-secret-key-here`
   - Add `CORS_ORIGINS` = `*` (or your actual frontend URL once deployed)
6. Disk (Important): Since you are using SQLite (`EDUPATH_ai.db`), you must attach a "Disk" in Render so the database isn't erased on every deployment. Set the mount path to `/opt/render/project/src/backend` and update your `DATABASE_URL` to `sqlite:////opt/render/project/src/backend/EDUPATH_ai.db`.

> **WARNING**
> SQLite is great for early stages, but as you scale, you should migrate to a PostgreSQL database (Render provides a free managed Postgres database). We already have psycopg installed, so switching is as easy as changing the DATABASE_URL environment variable!

## 2. Frontend Deployment (Vercel or Netlify)
For a React application, Vercel is the industry standard. It's incredibly fast, free, and provides automatic HTTPS.

**Steps for Vercel:**
1. Create an account on Vercel.com and connect your GitHub account.
2. Click **Add New Project** and import your EDUPATH repository.
3. Configuration:
   - **Framework Preset:** `Create React App`
   - **Root Directory:** `frontend`
4. Environment Variables:
   - Add `REACT_APP_API_BASE_URL` = `https://your-backend-url-from-render.onrender.com` (Make sure you don't have a trailing slash!)
5. Click **Deploy**. Vercel will build the React app and give you a live public URL (e.g., `https://edupath-ai.vercel.app`).

## 3. Post-Deployment Checklist
- Ensure your backend `CORS_ORIGINS` includes your new Vercel frontend URL.
- Visit the Vercel URL and submit a test student profile.
- Ensure the Machine Learning model returns a prediction successfully.
- Visit the `/admin` route on your live site and log in with `Shreekrishna@2003` and `Radhakrishna@2003`.

> **TIP**
> **Custom Domain:** Both Vercel and Render allow you to attach a custom domain (like www.edupath.com) for a professional startup look. You can buy one from Namecheap or GoDaddy and link it in the project settings!
