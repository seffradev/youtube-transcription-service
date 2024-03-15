// Code generated by sqlc. DO NOT EDIT.
// versions:
//   sqlc v1.25.0

package internal

import (
	"database/sql"
	"database/sql/driver"
	"fmt"
	"time"
)

type TranscriptionStatus string

const (
	TranscriptionStatusPending    TranscriptionStatus = "pending"
	TranscriptionStatusInProgress TranscriptionStatus = "in_progress"
	TranscriptionStatusCompleted  TranscriptionStatus = "completed"
	TranscriptionStatusFailed     TranscriptionStatus = "failed"
)

func (e *TranscriptionStatus) Scan(src interface{}) error {
	switch s := src.(type) {
	case []byte:
		*e = TranscriptionStatus(s)
	case string:
		*e = TranscriptionStatus(s)
	default:
		return fmt.Errorf("unsupported scan type for TranscriptionStatus: %T", src)
	}
	return nil
}

type NullTranscriptionStatus struct {
	TranscriptionStatus TranscriptionStatus
	Valid               bool // Valid is true if TranscriptionStatus is not NULL
}

// Scan implements the Scanner interface.
func (ns *NullTranscriptionStatus) Scan(value interface{}) error {
	if value == nil {
		ns.TranscriptionStatus, ns.Valid = "", false
		return nil
	}
	ns.Valid = true
	return ns.TranscriptionStatus.Scan(value)
}

// Value implements the driver Valuer interface.
func (ns NullTranscriptionStatus) Value() (driver.Value, error) {
	if !ns.Valid {
		return nil, nil
	}
	return string(ns.TranscriptionStatus), nil
}

type Transcription struct {
	ID          string
	Status      TranscriptionStatus
	Text        sql.NullString
	RequestedAt time.Time
	CompletedAt sql.NullTime
}