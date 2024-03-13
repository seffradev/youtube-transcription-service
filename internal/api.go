package internal

import (
	"log"
	"net/http"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gin-gonic/gin"
)

func url(c *gin.Context, producer *kafka.Producer) {
	topic := "transcription"
	id := c.Param("id")
	log.Println("URL ID:", id)
	producer.Produce(&kafka.Message{
		TopicPartition: kafka.TopicPartition{Topic: &topic, Partition: kafka.PartitionAny},
		Key:            []byte(id),
		Value:          []byte("pending"),
	}, nil)
	c.JSON(http.StatusAccepted, gin.H{"url": id})
}

func Api(engine *gin.Engine, producer *kafka.Producer) {
	api := engine.Group("/api", gin.BasicAuth(gin.Accounts{
		"foo":    "bar",
		"austin": "1234",
		"lena":   "hello2",
		"manu":   "4321",
	}))

	api.GET("/url/:id", func(c *gin.Context) {
		url(c, producer)
	})
}
