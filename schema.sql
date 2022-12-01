CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE IF NOT EXISTS tblReference (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES Users,
    reference_id TEXT,
    reference_name TEXT,

    address TEXT,
    -- annote ei käytetty
    author TEXT,
    booktitle TEXT,
    chapter TEXT,

    -- crossref ei käytetty
    edition TEXT,
    editor TEXT,
    howpublished TEXT,
    institution TEXT,

    journal TEXT,
    -- key ei käytetty
    month TEXT,
    note TEXT,
    number TEXT,

    organization TEXT,
    pages TEXT,
    publisher TEXT,
    school TEXT,
    series TEXT,

    title TEXT,
    type TEXT,
    volume TEXT,
    year TEXT,

    UNIQUE(user_id, reference_id)
);