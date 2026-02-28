CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

INSERT INTO users (username, email, password_hash) VALUES 
('jdoe', 'jdoe@example.com', 'hash1'),
('asmith', 'asmith@example.com', 'hash2'),
('bwayne', 'bwayne@example.com', 'hash3'),
('ckent', 'ckent@example.com', 'hash4'),
('dprince', 'dprince@example.com', 'hash5')
ON CONFLICT (username) DO NOTHING;

CREATE TABLE IF NOT EXISTS category (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name TEXT NOT NULL UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO category (name) VALUES
('General'),
('Science'),
('History'),
('Technology'),
('Geography')
ON CONFLICT (name) DO NOTHING;

CREATE TYPE question_type AS ENUM ('multiple', 'truefalse');

CREATE TABLE IF NOT EXISTS questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question TEXT NOT NULL,
    type question_type NOT NULL,
    options TEXT[],
    answer TEXT NOT NULL,
    category_id UUID REFERENCES category(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);

INSERT INTO questions (question, type, options, answer, category_id) VALUES
('What is the capital of France?', 'multiple', ARRAY['Berlin','Madrid','Paris','Rome'], 'Paris', (SELECT id FROM category WHERE name = 'Geography')),
('Python is a compiled language.', 'truefalse', NULL, 'False', (SELECT id FROM category WHERE name = 'Technology')),
('Which data structure uses LIFO?', 'multiple', ARRAY['Queue','Stack','Heap','Tree'], 'Stack', (SELECT id FROM category WHERE name = 'Technology')),
('HTTP is stateless.', 'truefalse', NULL, 'True', (SELECT id FROM category WHERE name = 'Technology'));