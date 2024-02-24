package internal

import "github.com/gin-gonic/gin"

func noRoute(c *gin.Context) {
	c.HTML(404, "404.html", gin.H{})
}

func Error(engine *gin.Engine) {
	engine.NoRoute(noRoute)
}
