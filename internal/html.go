package internal

import "github.com/gin-gonic/gin"

func Html(engine *gin.Engine, queries *Queries) {
	engine.LoadHTMLGlob("./web/templates/*")
	engine.GET("/", func(c *gin.Context) {
		c.HTML(200, "index.tmpl", gin.H{})
	})
	engine.GET("/transcriptions/:id", func(c *gin.Context) {
        id := c.Param("id")
        transcription, err := queries.GetTranscription(c, id)
        if err != nil {
            c.HTML(404, "404.tmpl", gin.H{})
            return
        }

		c.HTML(200, "transcriptions.tmpl", gin.H{"transcription": transcription})
	})
}
