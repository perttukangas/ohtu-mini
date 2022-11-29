CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS Article_Ref (
    id SERIAL PRIMARY KEY,
    ref_id TEXT,
    user_id INTEGER REFERENCES Users,
    author TEXT,
    heading TEXT,
    magazine TEXT,
    year TEXT,
    volume TEXT,
    doi TEXT,
    publisher TEXT,
    pages TEXT,
    UNIQUE (user_id, ref_id)
    
);