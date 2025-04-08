package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func RegisterAdminRoutes(r *gin.Engine) {
	r.GET("/admin", func(c *gin.Context) {
		cookie, err := c.Cookie("session_id")

		if err != nil || cookie == "" {
			c.HTML(http.StatusOK, "login_page", gin.H{
				"title": "Login",
			})
			return
		}

		c.HTML(http.StatusOK, "dashboard_page", gin.H{
			"title":      "Dashboard",
			"session_id": cookie,
		})
	})
}
