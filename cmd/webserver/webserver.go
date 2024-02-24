package main

import (
	"log"
	"yts/internal"

	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func main() {
	ip, port, err := internal.Environment()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	router := gin.Default()

	router.Use(static.Serve("/", static.LocalFile("./public", true)))
	internal.Auth(router)
	internal.Api(router)

	router.Run(ip + ":" + port)
}
