package internal

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func url(c *gin.Context) {
	c.JSON(http.StatusAccepted, gin.H{"url": c.Param("id")})
}

func Api(engine *gin.Engine) {
	api := engine.Group("/api", gin.BasicAuth(gin.Accounts{
		"foo":    "bar",
		"austin": "1234",
		"lena":   "hello2",
		"manu":   "4321",
	}))

	api.GET("/url/:id", url)
}
