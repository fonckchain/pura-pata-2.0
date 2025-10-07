# Pura Pata 🐕

Plataforma web para ayudar a perros a encontrar un hogar en Costa Rica.

## Tech Stack

- **Frontend**: Next.js 14 (TypeScript), Tailwind CSS
- **Backend**: FastAPI (Python 3.12)
- **Database**: PostgreSQL (Supabase)
- **Storage**: Supabase Storage
- **Auth**: Supabase Auth
- **Maps**: Google Maps API

## Estructura del Proyecto

```
pura-pata/
├── frontend/          # Next.js 14 application
├── backend/           # FastAPI application
├── database/          # Database initialization scripts
└── docker-compose.yml # Docker orchestration
```

## Prerequisitos

- Docker & Docker Compose
- Node.js 20+ (para desarrollo local)
- Python 3.12+ (para desarrollo local)
- Cuenta de Supabase
- Google Maps API Key

## Configuración Inicial

1. **Clonar el repositorio**
   ```bash
   git clone <repository-url>
   cd pura-pata-2.0
   ```

2. **Configurar variables de entorno**
   ```bash
   cp .env.example .env
   ```

   Editar `.env` con tus credenciales:
   - Supabase URL y keys
   - Google Maps API key
   - Secret key para JWT

3. **Configurar Supabase**
   - Crear un nuevo proyecto en Supabase
   - Crear un bucket llamado `dog-photos` en Storage
   - Habilitar autenticación por email
   - Copiar las credenciales al `.env`

## Ejecutar con Docker

```bash
# Construir y levantar todos los servicios
docker-compose up --build

# Servicios disponibles:
# - Frontend: http://localhost:3000
# - Backend API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - PostgreSQL: localhost:5432
```

## Desarrollo Local

### Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar en modo desarrollo
npm run dev
```

## Migraciones de Base de Datos

```bash
cd backend

# Crear nueva migración
alembic revision --autogenerate -m "description"

# Aplicar migraciones
alembic upgrade head

# Revertir última migración
alembic downgrade -1
```

## Características MVP

### Autenticación
- ✅ Registro con email/contraseña
- ✅ Login/Logout
- ✅ Recuperación de contraseña
- ✅ Perfil de usuario

### Publicación de Perros
- ✅ Formulario completo con validaciones
- ✅ Upload de fotos (1-5 imágenes)
- ✅ Upload de certificado veterinario (PDF)
- ✅ Selección de ubicación en mapa
- ✅ Editar/eliminar publicaciones

### Búsqueda y Filtros
- ✅ Mapa interactivo de Costa Rica
- ✅ Lista de perros disponibles
- ✅ Filtros por tamaño, edad, género, ubicación
- ✅ Búsqueda por provincia/radio

### Estados del Perro
- Disponible → Reservado → Adoptado
- ✅ Historial de cambios con timestamps
- ✅ Confirmación antes de marcar adoptado

### Contacto
- ✅ Botón de WhatsApp con mensaje pre-llenado
- ✅ Teléfono de contacto visible
- ✅ Compartir en redes sociales

## API Endpoints

### Autenticación
- `POST /api/v1/auth/register` - Registro de usuario
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/logout` - Logout

### Perros
- `GET /api/v1/dogs` - Listar perros (con filtros)
- `GET /api/v1/dogs/{id}` - Detalle de perro
- `POST /api/v1/dogs` - Crear publicación
- `PUT /api/v1/dogs/{id}` - Editar publicación
- `DELETE /api/v1/dogs/{id}` - Eliminar publicación
- `PATCH /api/v1/dogs/{id}/status` - Cambiar estado

### Usuarios
- `GET /api/v1/users/me` - Perfil actual
- `PUT /api/v1/users/me` - Actualizar perfil
- `GET /api/v1/users/me/dogs` - Mis publicaciones

### Uploads
- `POST /api/v1/uploads/photo` - Subir foto
- `POST /api/v1/uploads/certificate` - Subir certificado
- `DELETE /api/v1/uploads/{file_id}` - Eliminar archivo

## Roadmap Post-MVP

- [ ] AI para validación de imágenes
- [ ] AI para detección de raza
- [ ] AI para generación de descripciones
- [ ] Sistema de mensajería interno
- [ ] Notificaciones por email
- [ ] Panel de administración
- [ ] Estadísticas y analytics

## Licencia

MIT License - Ver [LICENSE](LICENSE)

## Contribuir

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Contacto

Proyecto Pura Pata - Ayudando a perros a encontrar un hogar en Costa Rica 🇨🇷
