package internal

import "github.com/gin-gonic/gin"

func Html(engine *gin.Engine) {
	engine.LoadHTMLGlob("./web/templates/*")
	engine.GET("/", func(c *gin.Context) {
		c.HTML(200, "index.tmpl", gin.H{})
	})
	})
}
