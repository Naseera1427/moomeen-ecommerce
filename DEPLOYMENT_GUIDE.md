# MOOMEEN PRODUCTS - Firebase & Google Cloud Deployment Guide
**Project ID:** `moomeen-69cf9`  
**Architecture:** Google Cloud Run (Django Backend) + Firebase Hosting (CDN & Rewrites) + PostgreSQL + Firebase Storage

---

## Why this Architecture?
- **Firebase Hosting alone** is a static file CDN and cannot execute Python / Django WSGI code.
- **Google Cloud Run** runs your full Django application in a serverless container that autoscales from 0 to thousands of requests, keeping costs minimal while handling traffic spikes.
- **Firebase Hosting** acts as your lightning-fast front door: it serves static assets (`/static/**`) from edge cache and forwards all dynamic URLs (`/**`) to your Cloud Run container.
- **Firebase Storage (Google Cloud Storage)** holds all uploaded product and category media files permanently.

---

## Step 1: Database Setup (PostgreSQL)

You have two simple options for PostgreSQL:

### Option A: Serverless PostgreSQL (Fastest & Free Tier Available)
1. Create a free PostgreSQL database on [Neon.tech](https://neon.tech) or [Supabase.com](https://supabase.com).
2. Copy your connection URI, for example:
   ```text
   DATABASE_URL=postgresql://user:password@ep-sample-12345.ap-southeast-1.aws.neon.tech/moomeen?sslmode=require
   ```

### Option B: Google Cloud SQL (PostgreSQL inside GCP)
1. Go to the [Google Cloud Console - Cloud SQL](https://console.cloud.google.com/sql/instances?project=moomeen-69cf9).
2. Click **Create Instance** &rarr; Select **PostgreSQL**.
3. Set Instance ID to `moomeen-db` and set a root password.
4. Choose the region `asia-south1` (Mumbai) or your preferred region.

---

## Step 2: Enable Firebase Storage (Media Files)

1. Open the [Firebase Console](https://console.firebase.google.com/project/moomeen-69cf9/overview).
2. In the left sidebar, click **Build** &rarr; **Storage** &rarr; **Get started**.
3. Choose standard mode and select region `asia-south1` (or match your Cloud Run region).
4. Note your bucket name (usually `moomeen-69cf9.firebasestorage.app` or `moomeen-69cf9.appspot.com`).

---

## Step 3: Deploy using Google Cloud Shell (No Local Tools Needed!)

Since Docker and gcloud are not installed on your local Windows PC, use **Google Cloud Shell**. It is a free in-browser Linux terminal pre-loaded with `docker`, `gcloud`, `git`, and `firebase`.

1. Open [Google Cloud Console](https://console.cloud.google.com/?project=moomeen-69cf9).
2. Click the **Activate Cloud Shell** icon (`>_`) in the top navigation bar.
3. In Cloud Shell, clone your repository and navigate into it:
   ```bash
   git clone https://github.com/Naseera1427/moomeen-ecommerce.git
   cd moomeen-ecommerce
   ```
4. Set your active project:
   ```bash
   gcloud config set project moomeen-69cf9
   ```
5. Enable required Google Cloud APIs:
   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com containerregistry.googleapis.com
   ```
6. Build and deploy the Docker container to Cloud Run:
   ```bash
   gcloud builds submit --config cloudbuild.yaml
   ```

---

## Step 4: Configure Cloud Run Environment Variables

1. Go to [Cloud Run in Google Cloud Console](https://console.cloud.google.com/run?project=moomeen-69cf9).
2. Click on the service **`moomeen-backend`** &rarr; **Edit & Deploy New Revision**.
3. Under the **Variables & Secrets** tab, add the following environment variables:

| Variable Name | Example Value | Description |
| :--- | :--- | :--- |
| `DJANGO_DEBUG` | `false` | Disables debug mode in production |
| `DJANGO_SECRET_KEY` | *(Generate a 50+ char random string)* | Production Django cryptographic key |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/moomeen` | PostgreSQL connection string |
| `GS_BUCKET_NAME` | `moomeen-69cf9.firebasestorage.app` | Firebase Storage bucket for images |
| `DJANGO_ALLOWED_HOSTS` | `moomeen-69cf9.web.app,moomeen-69cf9.firebaseapp.com` | Allowed hostnames |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://moomeen-69cf9.web.app,https://moomeen-69cf9.firebaseapp.com` | Trusted origins for forms |

4. Click **Deploy**.

---

## Step 5: Run Database Migrations & Create Superuser

From Cloud Shell:
```bash
# Run migrations using the deployed container image
gcloud run jobs create moomeen-migrate \
    --image gcr.io/moomeen-69cf9/moomeen-backend:latest \
    --region asia-south1 \
    --command python \
    --args manage.py,migrate \
    --set-env-vars DATABASE_URL="YOUR_DATABASE_URL_HERE",DJANGO_SECRET_KEY="YOUR_SECRET_KEY",DJANGO_DEBUG="false"

gcloud run jobs execute moomeen-migrate --region asia-south1 --wait
```

---

## Step 6: Deploy Firebase Hosting Rewrites

From Cloud Shell:
```bash
# Deploy Firebase Hosting routing
firebase deploy --only hosting --project moomeen-69cf9
```

Once completed, your full Django e-commerce platform will be live at:
- **`https://moomeen-69cf9.web.app`**
- **`https://moomeen-69cf9.firebaseapp.com`**
- (And any custom domain you connect under Firebase Hosting settings!)
