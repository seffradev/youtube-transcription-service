package internal

import "github.com/gin-gonic/gin"

func Html(engine *gin.Engine) {
	engine.LoadHTMLGlob("./web/templates/*")
	engine.GET("/", func(c *gin.Context) {
		c.HTML(200, "index.tmpl", gin.H{})
	})
	engine.GET("/login", func(c *gin.Context) {
		c.HTML(200, "login.tmpl", gin.H{})
	})
	engine.GET("/register", func(c *gin.Context) {
		c.HTML(200, "register.tmpl", gin.H{})
	})
}
