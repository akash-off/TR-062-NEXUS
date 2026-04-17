# Vercel Deployment Guide

## Structure for Vercel

```
/
├── api/                    # FastAPI backend
│   ├── main.py            # Entry point
│   ├── core/              # Configuration
│   ├── api/               # Routes
│   ├── models/            # ML models
│   ├── schemas/           # Data schemas
│   ├── services/          # Business logic
│   └── requirements.txt   # Python dependencies
│
├── frontend/              # React frontend
│   ├── package.json
│   └── public/
│
├── vercel.json            # Vercel deployment config
└── .python-version        # Python version
```

## Deploy to Vercel

### Using Vercel CLI

```bash
npm i -g vercel
vercel
```

### Using Git Integration

1. Push to GitHub/GitLab/Bitbucket
2. Import project in Vercel dashboard
3. Configure settings:
   - Framework: Other (Python)
   - Root Directory: ./
   - Build Command: (leave blank)
   - Output Directory: (leave blank)

### Environment Variables

Set in Vercel dashboard -> Settings -> Environment Variables:

```
DEBUG=False
API_TITLE=5G Nexus Slicer
API_VERSION=1.0.0
```

## API Endpoints

- **Base**: `https://your-domain.vercel.app/api`
- **Docs**: `https://your-domain.vercel.app/docs`
- **Health**: `https://your-domain.vercel.app/api/health`

## Notes

- FastAPI is served at the root `/`
- All requests are routed through `api/main.py`
- Frontend can be deployed separately or with the same Vercel project
