CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS Article_Ref (
    id SERIAL PRIMARY KEY,
    ref_id TEXT UNIQUE,
    user_id INTEGER REFERENCES Users,
    author TEXT,
    heading TEXT,
    year TEXT,
    magazine TEXT
    
);