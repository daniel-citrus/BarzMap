# BarzMap - Simple Tech Plan

## What We're Building
A web app where people can find and share outdoor gyms and workout parks. Users can see parks on a map, submit new locations, and admins can approve submissions.

## Tech Stack

### Frontend
- **React** - Makes the website interactive
- **MapLibre** - Shows the map with parks
- **Tailwind CSS** - Makes it look good
- **Vite** - Builds the website fast

### Backend
- **FastAPI** - Handles requests and data
- **Supabase** - Stores data and images
- **Auth0** - Handles user login
- **Python**

### Hosting
- **Vercel** - Hosts the website
- **Render** - Hosts the server
- **Supabase** - Hosts the database
- **Cloudflare** - Image delivery

## Features

### 1. User Finds Parks
```
User opens app → Sees map → Provide location → App shows nearby parks
```

### 2. User Submits New Park
```
User clicks "Add Park" → Fills out form → Uploads photos → Admin reviews → Park goes live
```

### 3. Admin Approves Parks
```
Admin logs in → Sees pending parks → Reviews each one → Approves or rejects
```

## Start Up Checklist

### 1. Set Up Accounts & Services
- [X] Create Supabase account and project
  - [X] Set up PostgreSQL database
  - [X] Configure authentication settings
  - [X] Create storage buckets for park images
- [X] Create Auth0 account and tenant
  - [X] Configure social login providers (Google, Facebook)
  - [X] Set up application settings and callbacks
  - [X] Configure user metadata and roles
- [X] Create Vercel account for frontend hosting
  - [X] Connect GitHub repository
  - [X] Configure build settings and environment variables
- [X] Create Render account for backend hosting
  - [X] Set up web service configuration
  - [X] Configure environment variables and secrets

### 2. Build Backend Foundation
- [X] Set up FastAPI project structure
  - [X] Create main.py with basic app configuration
  - [X] Set up project folders (api, models, services, utils)
  - [X] Configure CORS and middleware
- [X] Connect to Supabase database
  - [X] Install and configure Supabase Python client
  - [X] Set up database connection and authentication
  - [X] Create database models with SQLAlchemy
- [X] Create basic API endpoints
  - [X] Health check endpoint (/health)
  - [X] Parks CRUD endpoints (GET, POST, PUT, DELETE)
  - [X] Equipment endpoints for park management
- [ ] Implement user authentication endpoints
  - [ ] Auth0 JWT token validation middleware
  - [ ] Protected route decorators
  - [ ] User profile and metadata endpoints

### 3. Build Frontend Foundation
- [X] Set up React project with Vite
  - [X] Install and configure Tailwind CSS
  - [X] Set up project structure and components
  - [X] Configure build and development scripts
- [ ] Implement user authentication
  - [X] Install and configure Auth0 React SDK
  - [X] Create login/logout components
  - [X] Set up user profile display
  - [ ] Implement protected routes
    - [X] Extract Auth0 access token
    - [ ] Authorization header with payload
- [ ] Add map component
  - [ ] Install MapLibre GL JS
  - [ ] Create base map component with controls
  - [ ] Implement geolocation services
  - [ ] Add custom park markers and clustering
- [ ] Create park submission form
  - [ ] Design form with validation
  - [ ] Implement image upload functionality
  - [ ] Add location picker integration
  - [ ] Create submission confirmation flow

### 4. Connect Frontend to Backend
- [ ] Set up API communication
  - [ ] Install and configure Axios for HTTP requests
  - [ ] Create API service functions
  - [ ] Implement error handling and loading states
- [ ] Test core user flows
  - [ ] Test user registration and login
  - [ ] Test park data fetching and display
  - [ ] Test park submission workflow
  - [ ] Test admin approval process
- [ ] Implement real-time features
  - [ ] Set up Supabase real-time subscriptions
  - [ ] Add live updates for park submissions
  - [ ] Implement notification system

### 5. Post-Build Features & Polish
- [ ] Add routing and navigation
  - [ ] Install and configure React Router
  - [ ] Create page components (Home, Map, Submit, Profile)
  - [ ] Implement navigation menu and breadcrumbs
- [ ] Implement role-based access controls
  - [ ] Create admin dashboard
  - [ ] Add user role management
  - [ ] Implement permission-based UI rendering
- [ ] Add performance optimizations
  - [ ] Implement image lazy loading
  - [ ] Add caching strategies
  - [ ] Optimize bundle size and loading times

## Build Plan

### Phase 1: Foundation
#### Database & Backend Setup
- [ ] Design and create database schema
  - [ ] Parks table (id, name, location, coordinates, description, status)
  - [ ] Equipment table (id, park_id, type, condition, notes)
  - [ ] Users table (id, auth0_id, email, role, created_at)
  - [ ] Park_images table (id, park_id, image_url, uploaded_by, created_at)
- [ ] Set up database migrations and seeding
- [ ] Create comprehensive API documentation
- [ ] Implement proper error handling and logging

#### Frontend Foundation
- [ ] Set up component architecture
  - [ ] Create reusable UI components (Button, Input, Modal, Card)
  - [ ] Set up routing structure with React Router
  - [ ] Implement responsive layout with Tailwind CSS
- [ ] Basic website with map integration
  - [ ] Install and configure MapLibre GL JS
  - [ ] Create base map component with default styling
  - [ ] Add basic map controls (zoom, pan, fullscreen)
- [ ] User authentication system
  - [ ] Implement login/logout functionality
  - [ ] Create user profile management
  - [ ] Set up protected routes and role-based access

### Phase 2: Core Features
#### Park Discovery System
- [ ] Show parks on interactive map
  - [ ] Fetch parks from API and display as markers
  - [ ] Implement custom park markers with different icons
  - [ ] Add park clustering for performance with many locations
  - [ ] Create park details popup/modal with key information
- [ ] Park search and filtering
  - [ ] Add search bar with location and keyword search
  - [ ] Implement equipment type filtering
  - [ ] Add distance-based filtering (within X miles)
  - [ ] Create advanced search with multiple criteria

#### Park Submission System
- [ ] Submit new parks functionality
  - [ ] Create comprehensive park submission form
  - [ ] Implement location picker with map integration
  - [ ] Add equipment selection and description fields
  - [ ] Create image upload with drag-and-drop interface
- [ ] Form validation and user experience
  - [ ] Real-time form validation with helpful error messages
  - [ ] Progress indicators for form completion
  - [ ] Submission confirmation and tracking system
  - [ ] Email notifications for submission status updates

#### Basic Park Management
- [ ] Create basic park list view
  - [ ] Display parks in card/list format with key details
  - [ ] Add sorting options (distance, name, date added)
  - [ ] Implement pagination for large datasets
  - [ ] Add park favoriting and personal lists

### Phase 3: Admin Features
#### Admin Authentication & Dashboard
- [ ] Admin login and role management
  - [ ] Implement admin role detection and access control
  - [ ] Create admin-only routes and components
  - [ ] Set up admin dashboard with overview statistics
  - [ ] Add user management interface for admins

#### Content Moderation System
- [ ] Review pending parks interface
  - [ ] Create admin dashboard showing all pending submissions
  - [ ] Implement side-by-side review interface (submission vs existing)
  - [ ] Add bulk selection and action capabilities
  - [ ] Create detailed submission review with all metadata
- [ ] Approve/reject parks workflow
  - [ ] Implement approval/rejection with custom comments
  - [ ] Add reason codes for rejections (duplicate, inaccurate, inappropriate)
  - [ ] Create notification system for submitters
  - [ ] Implement park editing capabilities for admins

#### Image Management
- [ ] Upload and manage images
  - [ ] Implement image compression and optimization
  - [ ] Add image metadata and tagging system
  - [ ] Create image moderation tools (flag inappropriate content)
  - [ ] Set up automated image processing (thumbnails, resizing)

### Phase 4: Polish & Launch
#### User Experience Improvements
- [ ] Make it look good and professional
  - [ ] Implement consistent design system and branding
  - [ ] Add loading states and skeleton screens
  - [ ] Create smooth animations and transitions
  - [ ] Optimize for mobile devices and touch interactions
- [ ] Performance optimization
  - [ ] Implement lazy loading for images and components
  - [ ] Add caching strategies for API calls
  - [ ] Optimize bundle size and loading times
  - [ ] Set up CDN for static assets

#### Testing & Quality Assurance
- [ ] Comprehensive testing
  - [ ] Test all user flows and edge cases
  - [ ] Perform cross-browser compatibility testing
  - [ ] Test on various devices and screen sizes
  - [ ] Conduct accessibility testing (WCAG compliance)
- [ ] Bug fixes and stability
  - [ ] Fix identified bugs and issues
  - [ ] Implement proper error boundaries
  - [ ] Add comprehensive logging and monitoring
  - [ ] Set up automated testing pipeline

#### Launch Preparation
- [ ] Launch to users
  - [ ] Deploy to production environments
  - [ ] Set up monitoring and alerting systems
  - [ ] Create user documentation and help system
  - [ ] Prepare marketing materials and launch strategy
- [ ] Post-launch support
  - [ ] Set up user feedback collection system
  - [ ] Create admin training materials
  - [ ] Plan for user onboarding and support
  - [ ] Establish maintenance and update procedures

## Key Features
### For Regular Users
- [ ] See parks on interactive map
- [ ] Submit new park locations
- [ ] View park details and photos
- [ ] Search for parks by location

### For Admins
- [ ] Review pending parks
- [ ] Approve or reject parks
- [ ] Manage user accounts
- [ ] View statistics

## Cost
- **Auth0**: Free for 7,500 users/month
- **Supabase**: Free for 500MB database
- **Vercel**: Free hosting
- **Render**: Free server hosting
- **Cloudflare**: Free image delivery

**Total cost: $0/month** for the first 6+ months