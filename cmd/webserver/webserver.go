package main

import (
	"log"
	"yts/internal"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func main() {
	ip, port, bootstrapServers, err := internal.Environment()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	producer, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": bootstrapServers,
		"client.id":         "webserver",
		"acks":              "all",
	})

	if err != nil {
		log.Fatal("Failed to create Kafka producer:", err)
	}

	router := gin.Default()

	internal.Html(router)
	internal.Auth(router)
	internal.Api(router, producer)
	internal.Error(router)
	router.Use(static.Serve("/", static.LocalFile("./web/static", true)))

	router.Run(ip + ":" + port)
}
