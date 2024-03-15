CREATE TABLE transcription (
    id VARCHAR(11) NOT NULL PRIMARY KEY ,
    status ENUM('pending', 'in_progress', 'completed', 'failed') NOT NULL,
    text TEXT,
    requested_at DATETIME NOT NULL DEFAULT now(),
    completed_at DATETIME,
    cost INT,
);
