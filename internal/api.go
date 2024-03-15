package internal

import (
	"database/sql"
	"log"
	"net/http"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gin-gonic/gin"
)

func transcribe(c *gin.Context, producer *kafka.Producer, queries *Queries) {
	topic := "transcription"
	id := c.Param("id")
	log.Println("URL ID:", id)

	// Check if the URL exists
	transcription, err := queries.GetTranscription(c, id)
	if err != nil {
		log.Println("URL ID not found:", id, "adding to queue")
		queries.CreateTranscription(c, id)
		producer.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
			Key:            []byte(id),
			Value:          []byte("pending"),
		}, nil)
		c.JSON(http.StatusAccepted, gin.H{"message": "URL added to queue"})
		return
	}

	if transcription.Status == "pending" {
		log.Println("URL ID already in queue:", id)
		c.JSON(http.StatusAccepted, gin.H{"message": "URL already in queue"})
		return
	}

	if transcription.Status == "failed" {
		log.Println("URL ID failed to transcribe:", id)
        updateTranscription := UpdateTranscriptionParams{
            ID: id,
            Status: TranscriptionStatusPending,
            Text: sql.NullString{},
        }

		result, err := queries.UpdateTranscription(c, updateTranscription)
		if err != nil {
			log.Println("Failed to update URL ID:", id)
			c.JSON(http.StatusInternalServerError, gin.H{"message": "Failed to update URL"})
			return
		}

        count, err := result.RowsAffected()

        if err != nil || count == 0 {
            log.Println("URL ID failed to transcribe:", id)
            c.JSON(http.StatusInternalServerError, gin.H{"message": "URL failed to transcribe"})
            return
        }

		producer.Produce(&kafka.Message{
			TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
			Key:            []byte(id),
			Value:          []byte("pending"),
		}, nil)

		c.JSON(http.StatusAccepted, gin.H{"message": "URL failed to transcribe"})
		return
	}

	// Check if the URL is already transcribed
	if transcription.Status == "completed" {
		log.Println("URL ID already transcribed:", id)
		c.JSON(http.StatusOK, gin.H{
			"message":       "URL already transcribed",
			"transcription": transcription.Text.String,
		})
		return
	}
}

func Api(engine *gin.Engine, producer *kafka.Producer, queries *Queries) {
	api := engine.Group("/api", gin.BasicAuth(gin.Accounts{
		"foo":    "bar",
		"austin": "1234",
		"lena":   "hello2",
		"manu":   "4321",
	}))

	api.GET("/transcribe/:id", func(c *gin.Context) {
		transcribe(c, producer, queries)
	})
}
