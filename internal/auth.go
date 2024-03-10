package internal

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func register(c *gin.Context) {
	name := c.PostForm("name")
	email := c.PostForm("email")
	password := c.PostForm("password")
	c.JSON(http.StatusOK, gin.H{"name": name, "email": email, "password": password})
}

func login(c *gin.Context) {
	email := c.PostForm("email")
	password := c.PostForm("password")
	c.JSON(http.StatusOK, gin.H{"email": email, "password": password})
}

func Auth(engine *gin.Engine) {
	auth := engine.Group("/auth")
	auth.POST("/register", register)
	auth.POST("/login", login)
}
