package internal

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func register(c *gin.Context) {
	username := c.PostForm("username")
	email := c.PostForm("email")
	password := c.PostForm("password")
	c.JSON(http.StatusOK, gin.H{"username": username, "email": email, "password": password})
}

func login(c *gin.Context) {
	username := c.PostForm("username")
	password := c.PostForm("password")
	c.JSON(http.StatusOK, gin.H{"username": username, "password": password})
}

func Auth(engine *gin.Engine) {
	auth := engine.Group("/auth")
	auth.POST("/register", register)
	auth.POST("/login", login)
}
