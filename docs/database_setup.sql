-- BarzMap Database Setup
-- Copy and paste this entire file into Supabase SQL Editor

-- 1. Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    auth0_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    profile_picture_url TEXT,
    role VARCHAR(50) DEFAULT 'user' CHECK (role IN ('user', 'moderator', 'admin')),
    join_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 2. Parks Table
CREATE TABLE parks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    latitude DECIMAL(10, 8) NOT NULL,
    longitude DECIMAL(11, 8) NOT NULL,
    address TEXT,
    city VARCHAR(255),
    state VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
    status VARCHAR(50) DEFAULT 'pending' CHECK (status IN ('pending', 'approved', 'rejected')),
    submitted_by UUID REFERENCES users(id) ON DELETE SET NULL,
    submit_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    approved_by UUID REFERENCES users(id) ON DELETE SET NULL,
    approved_at TIMESTAMP WITH TIME ZONE,
    admin_notes TEXT,
    rating DECIMAL(3, 2) CHECK (rating >= 0 AND rating <= 5),
    review_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 3. Equipment Table
CREATE TABLE equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    icon_name VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 4. Park_Equipment Table (Junction Table)
CREATE TABLE park_equipment (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    equipment_id UUID REFERENCES equipment(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(park_id, equipment_id)
);

-- 5. Images Table
CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    uploaded_by UUID REFERENCES users(id) ON DELETE SET NULL,
    image_url TEXT NOT NULL,
    thumbnail_url TEXT,
    alt_text VARCHAR(255),
    is_approved BOOLEAN DEFAULT FALSE,
    is_primary BOOLEAN DEFAULT FALSE,
    is_inappropriate BOOLEAN DEFAULT FALSE,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 6. Reviews Table
CREATE TABLE reviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    park_id UUID REFERENCES parks(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    is_approved BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(park_id, user_id)
);

-- Performance Indexes
CREATE INDEX idx_parks_status ON parks(status);
CREATE INDEX idx_parks_location ON parks(latitude, longitude);
CREATE INDEX idx_parks_submitted_by ON parks(submitted_by);
CREATE INDEX idx_parks_approved_by ON parks(approved_by);
CREATE INDEX idx_park_equipment_park_id ON park_equipment(park_id);
CREATE INDEX idx_images_park_id ON images(park_id);
CREATE INDEX idx_images_approved ON images(is_approved);
CREATE INDEX idx_reviews_park_id ON reviews(park_id);
CREATE INDEX idx_users_role ON users(role);

-- Sample Equipment Data
INSERT INTO equipment (id, name, description, icon_name) VALUES
    (gen_random_uuid(), 'Pull-up Bar', 'Horizontal bar for pull-ups and chin-ups', 'pull-up-bar'),
    (gen_random_uuid(), 'Gymnastics Rings', 'Suspension rings for advanced bodyweight training', 'gymnastics-rings'),
    (gen_random_uuid(), 'Push-up Bars', 'Elevated handles for push-ups and planks', 'push-up-bars'),
    (gen_random_uuid(), 'Ab Station', 'Station for abdominal and core exercises', 'ab-station'),
    (gen_random_uuid(), 'Parallel Bars', 'Parallel bars for dips, L-sits, and handstands', 'parallel-bars'),
    (gen_random_uuid(), 'Monkey Bars', 'Overhead bars for traversing and pull-ups', 'monkey-bars'),
    (gen_random_uuid(), 'Running Track', 'Designated path for running and jogging', 'running-track');

-- Success message
SELECT 'BarzMap database setup completed successfully!' as message;
