# 🔐 Guía de Variables de Entorno - Pura Pata

Este documento explica todas las variables de entorno necesarias para el proyecto.

---

## 📁 Estructura de Archivos

```
pura-pata/
├── .env                          # Para Docker Compose (local)
├── frontend/.env.local           # Frontend local (desarrollo sin Docker)
├── backend/.env                  # Backend local (desarrollo sin Docker)
└── ESTE_ARCHIVO.md
```

---

## 🎯 Variables para VERCEL (Frontend)

Cuando deploys el **frontend** en Vercel, necesitas configurar estas variables:

### Variables Públicas (NEXT_PUBLIC_*)

```bash
# Supabase (Frontend)
NEXT_PUBLIC_SUPABASE_URL=https://wuqistxhaknrikklsgea.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1cWlzdHhoYWtucmlra2xzZ2VhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3ODMyNzEsImV4cCI6MjA3NTM1OTI3MX0.H_Ka_-XR1DWp-jxRmpfHjslKFr4fDV0vWfPnZ_w2EAE

# Google Maps API
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyBXO9idH63dmeHLoeX8tYc7vFCWXQgRvj0

# Backend URL (CAMBIAR cuando deploys el backend)
NEXT_PUBLIC_API_URL=https://tu-backend.railway.app/api/v1
```

**⚠️ IMPORTANTE:**
- `NEXT_PUBLIC_API_URL` debe apuntar a tu backend en producción
- Inicialmente puedes dejarlo vacío hasta que deploys el backend
- Las variables `NEXT_PUBLIC_*` son **públicas** (se exponen al navegador)

---

## 🚂 Variables para RAILWAY (Backend)

Cuando deploys el **backend** en Railway, necesitas:

```bash
# Database (Railway lo provee automáticamente)
DATABASE_URL=${{Postgres.DATABASE_URL}}

# Supabase (Backend)
SUPABASE_URL=https://wuqistxhaknrikklsgea.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1cWlzdHhoYWtucmlra2xzZ2VhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3ODMyNzEsImV4cCI6MjA3NTM1OTI3MX0.H_Ka_-XR1DWp-jxRmpfHjslKFr4fDV0vWfPnZ_w2EAE
SUPABASE_JWT_SECRET=qPW/inJGuMHTAHwcQHqnJu1UAKKfv3ALZkDQOl9FmbWQYFNQ7ivOHrYYtgoeYxEyJsBGMMf13wFGBVOnQfV3hA==

# Security
SECRET_KEY=thisIseasy420$

# CORS (agregar tu dominio de producción)
ALLOWED_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com,http://localhost:3000

# Storage
SUPABASE_STORAGE_BUCKET=dog-photos
```

**⚠️ IMPORTANTE:**
- Railway crea automáticamente `DATABASE_URL` cuando agregas PostgreSQL
- Usa `${{Postgres.DATABASE_URL}}` para referenciarlo
- Cambia `ALLOWED_ORIGINS` con tu dominio real

---

## 🐳 Variables para Docker (Desarrollo Local)

Ya configuradas en `.env` en root:

```bash
# Supabase
SUPABASE_URL=https://wuqistxhaknrikklsgea.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1cWlzdHhoYWtucmlra2xzZ2VhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3ODMyNzEsImV4cCI6MjA3NTM1OTI3MX0.H_Ka_-XR1DWp-jxRmpfHjslKFr4fDV0vWfPnZ_w2EAE
SUPABASE_JWT_SECRET=qPW/inJGuMHTAHwcQHqnJu1UAKKfv3ALZkDQOl9FmbWQYFNQ7ivOHrYYtgoeYxEyJsBGMMf13wFGBVOnQfV3hA==
NEXT_PUBLIC_SUPABASE_URL=https://wuqistxhaknrikklsgea.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind1cWlzdHhoYWtucmlra2xzZ2VhIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3ODMyNzEsImV4cCI6MjA3NTM1OTI3MX0.H_Ka_-XR1DWp-jxRmpfHjslKFr4fDV0vWfPnZ_w2EAE

# Backend
SECRET_KEY=thisIseasy420$
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/pura_pata

# Google Maps
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyBXO9idH63dmeHLoeX8tYc7vFCWXQgRvj0
```

---

## 📝 Checklist de Deployment

### 1️⃣ Deploy Frontend en Vercel

1. Ve a [vercel.com](https://vercel.com)
2. Import tu repositorio de GitHub
3. **Root Directory:** `frontend`
4. **Framework Preset:** Next.js
5. Agrega estas variables de entorno:
   ```
   NEXT_PUBLIC_SUPABASE_URL
   NEXT_PUBLIC_SUPABASE_ANON_KEY
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY
   NEXT_PUBLIC_API_URL (temporal: deja vacío o usa http://localhost:8000/api/v1)
   ```
6. Deploy!

### 2️⃣ Deploy Backend en Railway

1. Ve a [railway.app](https://railway.app)
2. New Project → Deploy from GitHub
3. Selecciona tu repo
4. **Root Directory:** `backend`
5. Agrega servicio PostgreSQL
6. Agrega estas variables:
   ```
   DATABASE_URL=${{Postgres.DATABASE_URL}}
   SUPABASE_URL
   SUPABASE_KEY
   SUPABASE_JWT_SECRET
   SECRET_KEY
   ALLOWED_ORIGINS (incluye tu dominio de Vercel)
   SUPABASE_STORAGE_BUCKET=dog-photos
   ```
7. Copia la URL pública de Railway

### 3️⃣ Conectar Frontend con Backend

1. Vuelve a Vercel
2. Settings → Environment Variables
3. Actualiza `NEXT_PUBLIC_API_URL` con la URL de Railway
4. Redeploy el frontend

### 4️⃣ Configurar Dominio en Cloudflare

1. En Vercel: Settings → Domains → Add tu-dominio.com
2. Vercel te dará un CNAME
3. En Cloudflare: DNS → Add record:
   ```
   Type: CNAME
   Name: @ (o www)
   Target: cname.vercel-dns.com (o el que te dé Vercel)
   Proxy: ON (naranja)
   ```

---

## 🔒 Seguridad

### ⚠️ NUNCA subas estos archivos a GitHub:
- `.env`
- `frontend/.env.local`
- `backend/.env`

### ✅ SÍ sube estos archivos (son plantillas):
- `.env.example`
- `frontend/.env.local.example`
- `backend/.env.example`

---

## 🆘 Troubleshooting

### Frontend no se conecta al Backend
- Verifica que `NEXT_PUBLIC_API_URL` esté correcto
- Debe ser HTTPS en producción
- No debe terminar con `/`

### Error de CORS
- Agrega el dominio de Vercel a `ALLOWED_ORIGINS` en Railway
- Formato: `https://tu-app.vercel.app`

### Supabase Auth no funciona
- Verifica que `NEXT_PUBLIC_SUPABASE_URL` y `NEXT_PUBLIC_SUPABASE_ANON_KEY` sean correctos
- En Supabase dashboard, agrega tu dominio a "Allowed URLs"

---

## 📞 Contacto

Si tienes dudas, revisa los logs:
- **Vercel:** Dashboard → tu-proyecto → Deployments → View Function Logs
- **Railway:** Dashboard → tu-servicio → Deployments → View Logs
