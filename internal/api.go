package internal

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"gorm.io/gorm"
)

func url(c *gin.Context) {
	c.JSON(http.StatusAccepted, gin.H{"url": c.Param("id")})
}

func Api(engine *gin.Engine, db *gorm.DB) {
	api := engine.Group("/api", gin.BasicAuth(gin.Accounts{
		"foo":    "bar",
		"austin": "1234",
		"lena":   "hello2",
		"manu":   "4321",
	}))

	api.GET("/url/:id", url)
}
