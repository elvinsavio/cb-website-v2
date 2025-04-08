package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func RegisterClientRoutes(r *gin.Engine) {
	r.GET("/", func(c *gin.Context) {
		c.HTML(http.StatusOK, "landing_page", gin.H{
			"title": "Landing Page",
		})
	})
}
