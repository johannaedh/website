CREATE TABLE Users (
    id TEXT PRIMARY KEY CHECK (id SIMILAR TO '[0-9]{10}'),
    password TEXT NOT NULL
);

CREATE TABLE SavedData (
    id TEXT,
    velocity FLOAT,
    accuracy FLOAT,
    FOREIGN KEY (id) REFERENCES Users(id),
    PRIMARY KEY (id, velocity, accuracy)
);