# BarzMap - Technical Architecture Plan

## Project Overview
A public-facing web application for the Calisthenics community to discover and share outdoor gyms and workout parks. Users can view parks on an interactive map, submit new locations, and admins can approve/reject submissions.

## Tech Stack Decisions

### Frontend
- **React 18 + JavaScript** - Familiar, strong ecosystem (free) - *TypeScript ready for future migration*
- **Vite** - Build tool and dev server, faster than CRA (free)
- **MapLibre GL JS** - Modern, open-source, better performance than Leaflet (free)
- **Tailwind CSS** - Rapid UI development (free)
- **React Router** - Client-side routing (free)

### Backend
- **FastAPI** - Python, excellent performance, auto-docs, type safety (free)
- **Supabase** - Hosted PostgreSQL + PostGIS, real-time, auth (free tier: 500MB DB, 1GB storage)
- **SQLAlchemy** - ORM with async support (free)
- **Redis** - Caching, rate limiting (free via Supabase or self-hosted)

### Authentication & Storage
- **Auth0** - JWT-based, handles social logins, roles (free: 7,500 users/month)
- **Supabase Storage** - Image storage only (free: 1GB storage, 2GB bandwidth)
- **Cloudinary** - NSFW detection, image optimization (free: 25GB storage/bandwidth)

### Deployment
- **Vercel** - Frontend hosting (free tier: unlimited projects, 100GB bandwidth)
- **Render** - Backend hosting (free tier: 750 hours/month)
- **Supabase** - Database hosting (free tier: 500MB DB, 1GB storage, 50k users)
- **Cloudflare** - CDN for images (free tier: unlimited bandwidth)

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   Services      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
│                        │                        │
├─ MapLibre Map         ├─ Auth0 JWT Validation  ├─ Auth0
├─ Park List            ├─ PostGIS Queries       ├─ Supabase Storage
├─ Submission Form      ├─ Image Processing      ├─ Cloudinary
└─ Admin Panel          └─ Rate Limiting         └─ Maptiler
```

## Data Model

### Core Tables

```sql
-- Users (extends Auth0)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255),
    picture VARCHAR(500),
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Parks
CREATE TABLE parks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    rating DECIMAL(3, 2) DEFAULT 0.0,
    status VARCHAR(50) DEFAULT 'pending', -- pending, approved, rejected
    created_by VARCHAR(255) NOT NULL, -- Auth0 user ID
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Equipment
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(100) UNIQUE NOT NULL,
    icon VARCHAR(100),
    category VARCHAR(50) -- bars, benches, cardio, etc.
);

-- Park Equipment (junction)
CREATE TABLE park_equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    equipment_id UUID REFERENCES equipment(id) ON DELETE CASCADE,
    quantity INTEGER DEFAULT 1,
    UNIQUE(park_id, equipment_id)
);

-- Images
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    url VARCHAR(500) NOT NULL,
    supabase_path VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    is_nsfw BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Admin Actions
CREATE TABLE admin_actions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    admin_id VARCHAR(255) NOT NULL, -- Auth0 user ID
    action VARCHAR(50) NOT NULL, -- approve, reject
    reason TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

### Indexes for Performance

```sql
-- Geospatial indexes
CREATE INDEX idx_parks_location ON parks USING GIST (location);
CREATE INDEX idx_parks_status ON parks (status);
CREATE INDEX idx_parks_created_by ON parks (created_by);
CREATE INDEX idx_parks_created_at ON parks (created_at DESC);

-- Equipment indexes
CREATE INDEX idx_park_equipment_park_id ON park_equipment (park_id);
CREATE INDEX idx_park_equipment_equipment_id ON park_equipment (equipment_id);

-- Image indexes
CREATE INDEX idx_images_park_id ON images (park_id);
CREATE INDEX idx_images_approved ON images (is_approved, is_nsfw);
```

### Key Geospatial Queries

```sql
-- Find parks within radius (in meters)
SELECT 
    p.*,
    ST_Distance(p.location, ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography) as distance
FROM parks p
WHERE p.status = 'approved'
    AND ST_DWithin(
        p.location, 
        ST_SetSRID(ST_MakePoint($1, $2), 4326)::geography, 
        $3
    )
ORDER BY distance;

-- Find parks in bounding box
SELECT p.*
FROM parks p
WHERE p.status = 'approved'
    AND ST_Within(
        p.location,
        ST_MakeEnvelope($1, $2, $3, $4, 4326)
    );

-- Clustering query (for zoomed out views)
SELECT 
    ST_ClusterKMeans(location, 10) OVER () as cluster_id,
    COUNT(*) as point_count,
    ST_Centroid(ST_Collect(location)) as center
FROM parks
WHERE status = 'approved';
```

## API Endpoints

### Public Endpoints
```
GET  /api/parks                    # List parks with filters
GET  /api/parks/{id}               # Get park details
GET  /api/parks/nearby             # Find parks within radius
GET  /api/equipment                # List equipment types
POST /api/parks                    # Submit new park (auth required)
POST /api/parks/{id}/images        # Upload images (auth required)
```

### Admin Endpoints
```
GET  /api/admin/submissions        # Get pending submissions
POST /api/admin/parks/{id}/approve # Approve park
POST /api/admin/parks/{id}/reject  # Reject park with reason
GET  /api/admin/stats              # Admin dashboard stats
```

### Authentication Endpoints
```
GET  /api/auth/profile             # Get user profile
POST /api/auth/refresh             # Refresh token
```

## Image Processing Pipeline

### Flow
1. **Upload**: Frontend → Backend → Supabase Storage
2. **NSFW Scan**: Backend → Cloudinary Moderation API
3. **Approval**: Admin reviews flagged images
4. **Public**: Approved images visible on map

### Implementation
```python
# Backend image processing
async def process_image_upload(file: UploadFile, park_id: UUID):
    # 1. Upload to Supabase Storage
    supabase_path = await upload_to_supabase(file, park_id)
    
    # 2. NSFW detection via Cloudinary
    nsfw_result = await check_nsfw(supabase_path)
    
    # 3. Save to database
    image = Image(
        park_id=park_id,
        url=supabase_path,
        is_nsfw=nsfw_result.is_nsfw,
        is_approved=not nsfw_result.is_nsfw  # Auto-approve if clean
    )
    
    return image
```

## Frontend UX Plan

### Map View
- **MapLibre GL JS** with Maptiler tiles
- **Marker clustering** for performance
- **Custom markers** for different equipment types
- **Hover effects** showing park preview
- **Click to open** detailed modal

### List View
- **Sidebar** with park list
- **Distance sorting** from user location
- **Equipment filters** (checkboxes)
- **Search** by park name
- **Hover sync** with map markers

### Submission Flow
- **Location picker** (map click or coordinates)
- **Equipment selection** (multi-select with icons)
- **Image upload** (drag & drop, preview)
- **Form validation** (required fields, image limits)

### Admin Panel
- **Submission queue** with thumbnails
- **Bulk actions** (approve/reject multiple)
- **Reason modal** for rejections
- **Statistics dashboard**

## Security Controls

### Authentication
- **Auth0 JWT validation** on all protected endpoints
- **Role-based access** (user vs admin)
- **Token refresh** handling

### Input Validation
- **Pydantic models** for all API inputs
- **SQL injection prevention** via SQLAlchemy
- **XSS protection** via React sanitization
- **File upload limits** (size, type, count)

### Rate Limiting
- **Redis-based** rate limiting
- **IP-based** limits for public endpoints
- **User-based** limits for submissions

### Data Protection
- **No direct DB access** from frontend
- **Environment variables** for all secrets
- **CORS configuration** for production domains

## Cost Analysis & Optimization

### Free Tier Limits & Management

#### **Current Stack Cost: $0/month for MVP**
| Service | Free Tier | Usage Strategy |
|---------|-----------|----------------|
| **Auth0** | 7,500 users/month | Sufficient for 6-12 months |
| **Supabase** | 500MB DB, 1GB storage, 50k users | Optimize with image compression |
| **Cloudinary** | 25GB storage, 25GB bandwidth | Implement lazy loading |
| **Maptiler** | 100k map loads/month | Cache map tiles |
| **Vercel** | Unlimited projects, 100GB bandwidth | Perfect for frontend |
| **Render** | 750 hours/month | Sufficient for backend |

#### **Cost Optimization Strategies**

##### **Image Management**
```python
# Backend image optimization
async def optimize_image_upload(file: UploadFile):
    # 1. Compress before upload (reduce storage)
    compressed_image = await compress_image(file)
    
    # 2. Generate multiple sizes (reduce bandwidth)
    sizes = [('thumb', 150), ('medium', 800), ('large', 1200)]
    optimized_images = await generate_sizes(compressed_image, sizes)
    
    # 3. Lazy load in frontend
    return optimized_images
```

##### **Caching Strategy**
```python
# Redis caching for expensive queries
@cache(expire=300)  # 5 minutes
async def get_parks_in_bounds(bounds: dict):
    return await db.execute(geospatial_query)

# Frontend caching
const useParksCache = () => {
    const cache = new Map();
    return (key, fetcher) => {
        if (cache.has(key)) return cache.get(key);
        const data = fetcher();
        cache.set(key, data);
        return data;
    };
};
```

##### **API Call Optimization**
- **Batch requests** for multiple park data
- **Debounced search** to reduce API calls
- **Pagination** for large datasets
- **WebSocket** for real-time updates (Supabase real-time)

#### **When to Upgrade (Cost Thresholds)**

##### **Early Growth ($5-25/month)**
- **Render Pro**: $7/month (when free tier insufficient)
- **Supabase Pro**: $25/month (when DB > 500MB)

##### **Medium Growth ($50-150/month)**
- **Cloudinary Advanced**: $89/month (when > 25GB usage)
- **Auth0 Professional**: $23/month (when > 7,500 users)

##### **Large Scale ($500+/month)**
- **Supabase Team**: $599/month
- **Dedicated hosting**: $100-200/month

### Alternative Free Services

#### **Backup Options**
- **Database**: PlanetScale (free: 1GB, 1B reads/month)
- **Storage**: AWS S3 (free: 5GB storage, 20k requests)
- **CDN**: Cloudflare (free: unlimited bandwidth)
- **Backend**: Railway ($5/month minimum, no free tier)

#### **Self-Hosting Options**
- **PostgreSQL**: Docker container on VPS ($5-10/month)
- **Redis**: Docker container on same VPS
- **Backend**: VPS deployment ($5-10/month)

## Docker Setup

### Docker Compose Configuration

#### **Services Overview**
- **Frontend**: Vite + React development server (port 5173)
- **Backend**: FastAPI development server (port 8000)
- **Redis**: Caching and rate limiting (port 6379)
- **PostgreSQL**: Local development database (port 5432) - *Optional, can use Supabase*

#### **Development vs Production**
- **Development**: Uses Docker Compose for local development
- **Production**: Uses Supabase for database, Vercel/Render for hosting

### Docker Benefits
- ✅ **Consistent environment** across team members
- ✅ **Easy setup** - one command to start everything
- ✅ **Isolated services** - no conflicts with local installations
- ✅ **Production-like** - similar to deployment environment
- ✅ **Easy cleanup** - remove containers without affecting system

### Docker Files Structure
```
BarzMap/
├── docker-compose.yml          # Main orchestration
├── .dockerignore              # Exclude files from builds
├── frontend/
│   └── Dockerfile.dev         # Frontend development container
├── backend/
│   └── Dockerfile.dev         # Backend development container
└── scripts/
    └── init-db.sql            # Database initialization (optional)
```

## DevOps & Deployment

### Development Setup

#### **Option 1: Docker Compose (Recommended)**
```bash
# 1. Create Supabase project (online)
# 2. Get connection string from Supabase dashboard
# 3. Copy .env.example to .env and update with your keys

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up -d --build

# Access services
# Frontend: http://localhost:5173
# Backend API: http://localhost:8000
# Backend Docs: http://localhost:8000/docs
```

#### **Option 2: Local Development**
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Set DATABASE_URL to Supabase connection string
uvicorn main:app --reload

# Frontend (Vite + React)
cd frontend
npm install
npm run dev  # Starts Vite dev server
```

### Environment Variables
```bash
# Backend (.env)
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
AUTH0_DOMAIN=your-domain.auth0.com
AUTH0_API_AUDIENCE=your-api-identifier
SUPABASE_URL=your-supabase-url
SUPABASE_SERVICE_KEY=your-service-key
CLOUDINARY_URL=cloudinary://...

# Frontend (.env)
VITE_API_URL=http://localhost:8000
VITE_AUTH0_DOMAIN=your-domain.auth0.com
VITE_AUTH0_CLIENT_ID=your-client-id
VITE_MAPTILER_API_KEY=your-maptiler-key

# Cost Monitoring (optional)
ENABLE_COST_MONITORING=true
CLOUDINARY_USAGE_ALERT=80  # Alert at 80% of free tier
SUPABASE_USAGE_ALERT=80
```

### Production Deployment
- **Vercel**: Frontend hosting
- **Railway/Render**: Backend hosting
- **Supabase**: Database + storage
- **Cloudflare**: CDN for images

## 4-Week Execution Plan

### Week 1: Foundation
- [ ] Project infrastructure setup (Supabase + Auth0 + environment)
- [ ] Docker Compose configuration for development
- [ ] Backend foundation (FastAPI + database models + auth middleware)
- [ ] Database setup (migrations + sample data)
- [ ] Frontend foundation (Vite + React + Tailwind + routing)
- [ ] Authentication integration (login/logout + protected routes)
- [ ] Basic map integration (MapLibre + Maptiler tiles)

### Week 2: Core Features
- [ ] Park CRUD operations (API + frontend)
- [ ] Geospatial queries (nearby parks, distance sorting)
- [ ] Map markers with clustering
- [ ] List view with distance sorting
- [ ] Basic park submission form

### Week 3: Advanced Features
- [ ] Image upload to Supabase Storage
- [ ] NSFW detection pipeline
- [ ] Equipment selection interface
- [ ] Admin approval workflow
- [ ] Search and filtering

### Week 4: Polish & Deploy
- [ ] Performance optimization (caching, lazy loading)
- [ ] Error handling and validation
- [ ] Mobile responsiveness
- [ ] Testing and bug fixes
- [ ] Production deployment

## First PR Checklist

### 1. Project Infrastructure
1. [ ] Create Supabase project and get connection string
2. [ ] Set up Auth0 application and get credentials
3. [ ] Create project structure (frontend/backend folders)
4. [ ] Set up environment variables (.env files)

### 2. Docker Setup
1. [ ] Docker Compose configuration
2. [ ] Frontend Dockerfile.dev
3. [ ] Backend Dockerfile.dev
4. [ ] .dockerignore file
5. [ ] Test Docker setup with `docker-compose up -d`

### 3. Backend Foundation
1. [ ] FastAPI app with CORS setup
2. [ ] Database connection and models
3. [ ] Basic health check endpoint
4. [ ] Environment configuration
5. [ ] Auth0 JWT validation middleware

### 4. Database Setup
1. [ ] Run initial migration with core tables
2. [ ] Sample data insertion
3. [ ] Geospatial indexes creation (PostGIS pre-enabled)
4. [ ] Test database connection

### 5. Frontend Foundation
1. [ ] React app with Vite (JavaScript, TypeScript-ready structure)
2. [ ] Tailwind CSS configuration
3. [ ] Basic routing structure
4. [ ] Auth0 React SDK setup
5. [ ] MapLibre map integration

### 6. Authentication Integration
1. [ ] Backend JWT validation working
2. [ ] Frontend login/logout functionality
3. [ ] Protected route handling
4. [ ] User profile management
5. [ ] Test full auth flow

## TypeScript Migration Strategy

### MVP Phase (JavaScript)
- **Use `.js` files** with JSDoc comments for type hints
- **Consistent naming conventions** (camelCase for variables, PascalCase for components)
- **PropTypes** for component prop validation
- **Structured imports/exports** to match TypeScript patterns

### TypeScript Migration Path
```javascript
// MVP: JavaScript with JSDoc
/**
 * @typedef {Object} Park
 * @property {string} id
 * @property {string} name
 * @property {number} latitude
 * @property {number} longitude
 * @property {string} status
 */

/**
 * @param {Park} park
 * @returns {JSX.Element}
 */
function ParkMarker({ park }) {
  return <div>{park.name}</div>;
}

// Future: TypeScript migration
interface Park {
  id: string;
  name: string;
  latitude: number;
  longitude: number;
  status: string;
}

function ParkMarker({ park }: { park: Park }): JSX.Element {
  return <div>{park.name}</div>;
}
```

### Migration Checklist
- [ ] **File Structure**: Use TypeScript-compatible folder structure
- [ ] **Naming**: Follow TypeScript naming conventions from day one
- [ ] **Imports**: Use named imports/exports consistently
- [ ] **Props**: Use PropTypes for component validation
- [ ] **API Calls**: Structure API responses consistently
- [ ] **State Management**: Use predictable state patterns

### Migration Steps (Post-MVP)
1. **Install TypeScript**: `npm install --save-dev typescript @types/react @types/react-dom`
2. **Rename Files**: `.js` → `.tsx` for React components, `.js` → `.ts` for utilities
3. **Add Types**: Gradually add interfaces and types
4. **Fix Errors**: Address TypeScript compilation errors
5. **Enable Strict Mode**: Gradually enable stricter TypeScript settings

### JavaScript Best Practices for TypeScript Compatibility

#### **Component Structure**
```javascript
// ✅ Good: TypeScript-ready structure
import React from 'react';
import PropTypes from 'prop-types';

/**
 * Park marker component
 * @param {Object} props
 * @param {Park} props.park - Park data
 * @param {Function} props.onClick - Click handler
 */
function ParkMarker({ park, onClick }) {
  return (
    <div onClick={() => onClick(park.id)}>
      {park.name}
    </div>
  );
}

ParkMarker.propTypes = {
  park: PropTypes.shape({
    id: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    latitude: PropTypes.number.isRequired,
    longitude: PropTypes.number.isRequired,
  }).isRequired,
  onClick: PropTypes.func.isRequired,
};

export default ParkMarker;
```

#### **API Response Handling**
```javascript
// ✅ Good: Consistent API response structure
const API_ENDPOINTS = {
  PARKS: '/api/parks',
  PARK_DETAILS: (id) => `/api/parks/${id}`,
  NEARBY_PARKS: '/api/parks/nearby',
};

/**
 * Fetch parks data
 * @param {Object} params - Query parameters
 * @returns {Promise<Park[]>}
 */
async function fetchParks(params = {}) {
  const response = await fetch(`${API_ENDPOINTS.PARKS}?${new URLSearchParams(params)}`);
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  return response.json();
}
```

#### **State Management**
```javascript
// ✅ Good: Predictable state patterns
const initialState = {
  parks: [],
  loading: false,
  error: null,
  filters: {
    equipment: [],
    radius: 5000,
  },
};

function parksReducer(state, action) {
  switch (action.type) {
    case 'SET_LOADING':
      return { ...state, loading: action.payload };
    case 'SET_PARKS':
      return { ...state, parks: action.payload, loading: false };
    case 'SET_ERROR':
      return { ...state, error: action.payload, loading: false };
    default:
      return state;
  }
}
```

## Trade-offs & Decisions

### MapLibre vs Leaflet
- **MapLibre**: Better performance, vector tiles, modern features
- **Leaflet**: Simpler setup, more plugins, raster tiles
- **Decision**: MapLibre for better UX and future scalability

### FastAPI vs Node.js
- **FastAPI**: Python ecosystem, auto-docs, type safety
- **Node.js**: JavaScript full-stack, larger ecosystem
- **Decision**: FastAPI for Python familiarity and performance

### Supabase vs Direct Storage
- **Supabase**: Managed service, built-in auth integration
- **Direct S3/Cloudinary**: More control, potentially cheaper
- **Decision**: Supabase for simplicity and Auth0 integration

### Auth0 vs Custom Auth
- **Auth0**: Managed service, social logins, security best practices
- **Custom**: Full control, potentially cheaper
- **Decision**: Auth0 for security and development speed

### JavaScript vs TypeScript for MVP
- **JavaScript**: Faster development, less setup, familiar
- **TypeScript**: Better IDE support, type safety, fewer runtime errors
- **Decision**: JavaScript for MVP speed, TypeScript-ready structure for future migration

## Success Metrics

### Technical
- [ ] Map loads in <2 seconds
- [ ] API response time <200ms
- [ ] 99.9% uptime
- [ ] Zero security vulnerabilities
- [ ] Stay within free tier limits for 6+ months

### User Experience
- [ ] Users can find parks within 1km
- [ ] Submission process <5 minutes
- [ ] Admin approval <24 hours
- [ ] Mobile-friendly interface

### Business
- [ ] 100+ parks in first month
- [ ] 50+ active users
- [ ] 90% submission approval rate
- [ ] Positive user feedback

---

**Next Steps**: Start with the First PR Checklist, focusing on getting the basic infrastructure running before adding features.
