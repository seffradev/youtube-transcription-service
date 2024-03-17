package main

import (
	"database/sql"
	"log"
	"yts/internal"

	"github.com/confluentinc/confluent-kafka-go/kafka"
	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func main() {
	ip, port, bootstrapServers, databaseUrl, err := internal.Environment()
	if err != nil {
		log.Println("Error loading .env file")
	}

    db, err := sql.Open("mysql", databaseUrl)
    if err != nil {
        log.Fatal("Error connecting to database")
    }

    queries := internal.New(db)

	producer, err := kafka.NewProducer(&kafka.ConfigMap{
		"bootstrap.servers": bootstrapServers,
		"client.id":         "webserver",
		"acks":              "all",
	})

	if err != nil {
		log.Fatal("Failed to create Kafka producer:", err)
	}

	router := gin.Default()

	internal.Html(router, queries)
	internal.Auth(router)
	internal.Api(router, producer, queries)
	internal.Error(router)
	router.Use(static.Serve("/", static.LocalFile("./web/static", true)))

	router.Run(ip + ":" + port)
}
