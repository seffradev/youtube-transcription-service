-- name: GetTranscription :one
SELECT
    id,
    text,
    status,
    requested_at,
    completed_at
FROM
    transcription
WHERE
    id = ?
LIMIT 1;

-- name: ListTranscription :many
SELECT
    id,
    text,
    status,
    requested_at,
    completed_at
FROM
    transcription;

-- name: CreateTranscription :execresult
INSERT INTO
    transcription (id, status)
VALUES (
    ?,
    'pending'
);

-- name: UpdateTranscription :execresult
UPDATE
    transcription
SET
    text = ?,
    status = ?,
    completed_at = now()
WHERE
    id = ?;
