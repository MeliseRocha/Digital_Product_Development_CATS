-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Drop all existing tables (if needed)
DROP TABLE IF EXISTS appointments CASCADE;
DROP TABLE IF EXISTS care_link CASCADE;
DROP TABLE IF EXISTS clinics CASCADE;
DROP TABLE IF EXISTS employment_link CASCADE;
DROP TABLE IF EXISTS front_desk_users CASCADE;
DROP TABLE IF EXISTS healthcare_professionals CASCADE;
DROP TABLE IF EXISTS medical_records CASCADE;
DROP TABLE IF EXISTS patient_identifiers CASCADE;
DROP TABLE IF EXISTS patients CASCADE;
DROP TABLE IF EXISTS professional_identifiers CASCADE;
DROP TABLE IF EXISTS schedule_dates CASCADE;
DROP TABLE IF EXISTS schedules CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- ENUM Types
DO $$ BEGIN
    CREATE TYPE clinic_type_enum AS ENUM ('Public', 'Private', 'Mixed');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE status_enum AS ENUM ('active', 'inactive');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE patient_status_enum AS ENUM ('active', 'inactive', 'deceased');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE identifier_type_enum AS ENUM ('SUS', 'SSN', 'Insurance_ID', 'Passport_Number', 'CPF');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

DO $$ BEGIN
    CREATE TYPE professional_identifier_enum AS ENUM ('CRM', 'State_Medical_License', 'DEA', 'NPI', 'License', 'Certification');
EXCEPTION WHEN duplicate_object THEN NULL; END $$;

-- Table: users
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  username VARCHAR(50) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL UNIQUE,
  phone VARCHAR(20),
  password_hash VARCHAR(255) NOT NULL,
  status status_enum NOT NULL DEFAULT 'active',
  last_login TIMESTAMP DEFAULT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  healthcare_professional_id UUID UNIQUE,
  front_desk_user_id UUID UNIQUE,
  roles JSONB NOT NULL
);

-- Table: clinics
CREATE TABLE IF NOT EXISTS clinics (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name VARCHAR(100) NOT NULL,
  address TEXT NOT NULL,
  address_number VARCHAR(10) NOT NULL,
  address_complement VARCHAR(100),
  zip VARCHAR(20) NOT NULL,
  city VARCHAR(100) NOT NULL,
  state CHAR(2) NOT NULL,
  country CHAR(2) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(255),
  website VARCHAR(255),
  clinic_type clinic_type_enum NOT NULL DEFAULT 'Private',
  user_id UUID NOT NULL,
  created_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table: healthcare_professionals
CREATE TABLE IF NOT EXISTS healthcare_professionals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  profession VARCHAR(50) NOT NULL,
  full_name VARCHAR(300) NOT NULL,
  specialty VARCHAR(100),
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  address TEXT NOT NULL,
  address_number VARCHAR(10) NOT NULL,
  address_complement VARCHAR(100),
  created_at TIMESTAMP DEFAULT NULL,
  clinic_id UUID NOT NULL,
  FOREIGN KEY (clinic_id) REFERENCES clinics(id) ON DELETE CASCADE
);

-- Table: patients
CREATE TABLE IF NOT EXISTS patients (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  picture BYTEA,
  date_of_birth DATE NOT NULL,
  gender VARCHAR(10) NOT NULL,
  address TEXT NOT NULL,
  address_number VARCHAR(10) NOT NULL,
  address_complement VARCHAR(100),
  zip VARCHAR(20) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(100) NOT NULL,
  status patient_status_enum NOT NULL DEFAULT 'active',
  emergency_contact_name VARCHAR(100),
  emergency_contact_phone VARCHAR(20),
  nationality VARCHAR(50),
  language VARCHAR(50),
  insurance_provider VARCHAR(100),
  insurance_policy_number VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: medical_records
CREATE TABLE IF NOT EXISTS medical_records (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  record_date TIMESTAMP,
  diagnosis TEXT NOT NULL,
  anamnesis TEXT NOT NULL,
  evolution TEXT NOT NULL,
  pdf_file BYTEA,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  hash CHAR(64) NOT NULL,
  appointment_id UUID NOT NULL,
  care_link_id UUID NOT NULL,
  FOREIGN KEY (appointment_id) REFERENCES appointments(id) ON DELETE CASCADE,
  FOREIGN KEY (care_link_id) REFERENCES care_link(id)
);

-- Table: care_link
CREATE TABLE IF NOT EXISTS care_link (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clinic_id UUID NOT NULL,
  doctor_id UUID NOT NULL,
  patient_id UUID NOT NULL,
  status status_enum DEFAULT 'active',
  UNIQUE (clinic_id, doctor_id, patient_id),
  FOREIGN KEY (clinic_id) REFERENCES clinics(id) ON DELETE CASCADE,
  FOREIGN KEY (doctor_id) REFERENCES healthcare_professionals(id) ON DELETE CASCADE,
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE
);

-- Table: appointments
CREATE TABLE IF NOT EXISTS appointments (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  schedule_id UUID,
  appointment_date TIMESTAMP,
  confirmed BOOLEAN DEFAULT FALSE,
  care_link_id UUID,
  FOREIGN KEY (schedule_id) REFERENCES schedules(id),
  FOREIGN KEY (care_link_id) REFERENCES care_link(id)
);

-- Table: employment_link
CREATE TABLE IF NOT EXISTS employment_link (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  clinic_id UUID NOT NULL,
  doctor_id UUID NOT NULL,
  created_at TIMESTAMP DEFAULT NULL,
  FOREIGN KEY (clinic_id) REFERENCES clinics(id),
  FOREIGN KEY (doctor_id) REFERENCES healthcare_professionals(id)
);

-- Table: front_desk_users
CREATE TABLE IF NOT EXISTS front_desk_users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  is_admin BOOLEAN NOT NULL,
  clinic_id UUID NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT NULL,
  address TEXT,
  address_number VARCHAR(10),
  address_complement VARCHAR(100),
  FOREIGN KEY (clinic_id) REFERENCES clinics(id)
);

-- Table: patient_identifiers
CREATE TABLE IF NOT EXISTS patient_identifiers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  patient_id UUID NOT NULL,
  identifier_type identifier_type_enum NOT NULL,
  identifier_value VARCHAR(50) NOT NULL,
  FOREIGN KEY (patient_id) REFERENCES patients(id)
);

-- Table: professional_identifiers
CREATE TABLE IF NOT EXISTS professional_identifiers (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  professional_id UUID NOT NULL,
  identifier_type professional_identifier_enum NOT NULL,
  identifier_value VARCHAR(50) NOT NULL,
  FOREIGN KEY (professional_id) REFERENCES healthcare_professionals(id)
);

-- Table: schedules
CREATE TABLE IF NOT EXISTS schedules (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  doctor_id UUID NOT NULL,
  clinic_id UUID NOT NULL,
  available_from TIME NOT NULL,
  available_to TIME NOT NULL,
  appointment_interval INT NOT NULL,
  start_date DATE,
  end_date DATE,
  FOREIGN KEY (clinic_id) REFERENCES clinics(id),
  FOREIGN KEY (doctor_id) REFERENCES healthcare_professionals(id)
);

-- Table: schedule_dates
CREATE TABLE IF NOT EXISTS schedule_dates (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  schedule_id UUID NOT NULL,
  schedule_date DATE NOT NULL,
  break_start TIME,
  break_end TIME,
  start_time TIME NOT NULL,
  end_time TIME NOT NULL,
  FOREIGN KEY (schedule_id) REFERENCES schedules(id)
);