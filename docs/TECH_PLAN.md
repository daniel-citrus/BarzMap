# BarzMap - Simple Tech Plan

## What We're Building
A web app where people can find and share outdoor gyms and workout parks. Users can see parks on a map, submit new locations, and admins can approve submissions.

## Tech Stack (What We're Using)

### Frontend (What Users See)
- **React** - Makes the website interactive
- **MapLibre** - Shows the map with parks
- **Tailwind CSS** - Makes it look good
- **Vite** - Builds the website fast

### Backend (Server Stuff)
- **FastAPI** - Handles requests and data
- **Supabase** - Stores data and images
- **SQLAlchemy** - Talks to the database
- **Auth0** - Handles user login

### Where It Lives
- **Vercel** - Hosts the website
- **Render** - Hosts the server
- **Supabase** - Hosts the database
- **Cloudflare** - Makes images load fast

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
Admin logs in → Sees pending submissions → Reviews each one → Approves or rejects
```

## Database Tables

### Users
- User ID (Auth0), email, name, profile picture
- Role (user, moderator, admin)
- Join date

### Parks
- Park name, description, location
- Status (pending, approved, rejected)
- Submitted by
- Submit date
- Rating

### Equipment
- Equipment types (bars, benches, etc.)
- Which parks have what equipment

### Images
- Park photos
- Whether they're approved
- Whether they're inappropriate

## 4-Week Build Plan

### Week 1: Foundation
- [ ] Set up project structure
- [ ] Create database tables
- [ ] Basic website with map
- [ ] User login/logout

### Week 2: Core Features
- [ ] Show parks on map
- [ ] Submit new parks
- [ ] Basic park list

### Week 3: Admin Features
- [ ] Admin login
- [ ] Review submissions
- [ ] Approve/reject parks
- [ ] Upload images

### Week 4: Polish & Launch
- [ ] Make it look good
- [ ] Test everything
- [ ] Fix bugs
- [ ] Launch to users

## Key Features

### For Regular Users
- [ ] See parks on interactive map
- [ ] Submit new park locations
- [ ] View park details and photos
- [ ] Search for parks by location

### For Admins
- [ ] Review new submissions
- [ ] Approve or reject parks
- [ ] Manage user accounts
- [ ] View statistics

## Cost (Free to Start)
- **Auth0**: Free for 7,500 users/month
- **Supabase**: Free for 500MB database
- **Vercel**: Free hosting
- **Render**: Free server hosting
- **Cloudflare**: Free image delivery

**Total cost: $0/month** for the first 6+ months

## Getting Started Checklist

### 1. Set Up Accounts
- [X] Create Supabase account
- [X] Create Auth0 account
- [X] Create Vercel account
- [X] Create Render account

### 2. Build Backend
- [X] Set up FastAPI project
- [ ] Connect to Supabase database
- [ ] Create basic API endpoints
- [ ] Add user authentication

### 3. Build Frontend
- [ ] Set up React project
- [ ] Add map component
- [ ] Create park submission form
- [ ] Add user login

### 4. Connect Everything
- [ ] Connect frontend to backend
- [ ] Test user registration
- [ ] Test park submission
- [ ] Test admin approval

## Success Metrics
- [ ] 100+ parks in first month
- [ ] 50+ active users
- [ ] 90% submission approval rate
- [ ] App loads in under 3 seconds

## Next Steps
1. Start with Week 1 foundation
2. Get basic map working
3. Add user authentication
4. Build park submission feature
5. Add admin approval system
6. Launch and get feedback

---

**Goal**: Build a simple, working app that helps people find outdoor gyms. Focus on core features first, add complexity later.
