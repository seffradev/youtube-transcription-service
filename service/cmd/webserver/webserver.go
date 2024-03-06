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
		log.Print("Error loading .env file")
	}

	router := gin.Default()

	internal.Html(router)
	internal.Auth(router)
	internal.Api(router)
	internal.Error(router)
	router.Use(static.Serve("/", static.LocalFile("./web/public", true)))

	router.Run(ip + ":" + port)
}
