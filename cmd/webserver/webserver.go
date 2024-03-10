package main

import (
	"log"
	"yts/internal"

	"github.com/gin-gonic/contrib/static"
	"github.com/gin-gonic/gin"
)

func main() {
	ip, port, db_url, err := internal.Environment()
	if err != nil {
		log.Fatal("Error loading .env file")
	}

	db, err := internal.Database(db_url)
	if err != nil {
		log.Fatal("Error connecting to database")
	}

	router := gin.Default()

	internal.Html(router)
	internal.Auth(router)
	internal.Api(router, db)
	internal.Error(router)
	router.Use(static.Serve("/", static.LocalFile("./web/static", true)))

	router.Run(ip + ":" + port)
}
