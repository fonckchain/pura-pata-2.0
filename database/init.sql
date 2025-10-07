-- Database initialization script for Pura Pata
-- This script creates the necessary tables, indexes, and extensions

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable PostGIS for location queries (optional, for advanced geo queries)
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- Users table (managed by Supabase Auth, but we create a compatible version)
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  location VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Dogs table
CREATE TABLE IF NOT EXISTS dogs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

  -- Basic info
  name VARCHAR(100) NOT NULL,
  age_years INT NOT NULL,
  age_months INT DEFAULT 0,
  breed VARCHAR(100) NOT NULL,
  size VARCHAR(20) NOT NULL CHECK (size IN ('pequeño', 'mediano', 'grande')),
  gender VARCHAR(10) NOT NULL CHECK (gender IN ('macho', 'hembra')),
  color VARCHAR(100) NOT NULL,
  description TEXT,

  -- Health info
  vaccinated BOOLEAN DEFAULT FALSE,
  sterilized BOOLEAN DEFAULT FALSE,
  dewormed BOOLEAN DEFAULT FALSE,
  special_needs TEXT,

  -- Location
  latitude FLOAT NOT NULL,
  longitude FLOAT NOT NULL,
  address TEXT,
  province VARCHAR(50),

  -- Contact
  contact_phone VARCHAR(20) NOT NULL,
  contact_email VARCHAR(255),

  -- Media
  photos TEXT[] NOT NULL,
  certificate TEXT,

  -- Status
  status VARCHAR(20) DEFAULT 'disponible' NOT NULL CHECK (status IN ('disponible', 'reservado', 'adoptado')),

  -- Relations
  publisher_id UUID REFERENCES users(id) ON DELETE CASCADE,

  -- Timestamps
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  adopted_at TIMESTAMP
);

-- Indexes for dogs table
CREATE INDEX IF NOT EXISTS idx_dogs_status ON dogs(status);
CREATE INDEX IF NOT EXISTS idx_dogs_publisher ON dogs(publisher_id);
CREATE INDEX IF NOT EXISTS idx_dogs_province ON dogs(province);
CREATE INDEX IF NOT EXISTS idx_dogs_created_at ON dogs(created_at DESC);

-- Dog status history table
CREATE TABLE IF NOT EXISTS dog_status_history (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  dog_id UUID REFERENCES dogs(id) ON DELETE CASCADE,
  old_status VARCHAR(20),
  new_status VARCHAR(20) NOT NULL,
  changed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_status_history_dog ON dog_status_history(dog_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to automatically update updated_at
CREATE TRIGGER update_dogs_updated_at BEFORE UPDATE ON dogs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Function to log status changes
CREATE OR REPLACE FUNCTION log_dog_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO dog_status_history (dog_id, old_status, new_status)
        VALUES (NEW.id, OLD.status, NEW.status);

        -- Set adopted_at when status changes to adoptado
        IF NEW.status = 'adoptado' AND OLD.status != 'adoptado' THEN
            NEW.adopted_at = NOW();
        END IF;
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger to log status changes
CREATE TRIGGER log_status_change BEFORE UPDATE ON dogs
    FOR EACH ROW EXECUTE FUNCTION log_dog_status_change();

-- Sample provinces in Costa Rica
COMMENT ON COLUMN dogs.province IS 'Provincias: San José, Alajuela, Cartago, Heredia, Guanacaste, Puntarenas, Limón';
