DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS authors;
DROP TABLE IF EXISTS translators;
DROP TABLE IF EXISTS subjects;
DROP TABLE IF EXISTS formats;

-- Leaving out bookshelves and languages for now

CREATE TABLE books (
    book_id INTEGER PRIMARY KEY,
    title TEXT,
    download_count INTEGER,
    author_ids TEXT,    -- Maybe do this as CSV? 
    translator_ids TEXT,
    subject_ids TEXT,
    format_ids TEXT
);

CREATE TABLE authors (
    author_id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT UNIQUE,
    birth_year INTEGER,
    death_year INTEGER
);

CREATE TABLE translators (
    translator_id INTEGER PRIMARY KEY AUTOINCREMENT,
    translator_name TEXT UNIQUE,
    birth_year INTEGER,
    death_year INTEGER
);

CREATE TABLE subjects (
    subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_name TEXT UNIQUE
);

CREATE TABLE formats (
    format_id INTEGER PRIMARY KEY AUTOINCREMENT,
    format_type TEXT,
    format_link TEXT
);