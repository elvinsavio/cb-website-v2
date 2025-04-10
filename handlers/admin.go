package handlers

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func RenderLoginPage(c *gin.Context) {
	c.HTML(http.StatusOK, "login_page", gin.H{})
}

func RenderAdminDashboard(c *gin.Context) {
	_, err := c.Request.Cookie("session")

	if err != nil {
		c.Redirect(http.StatusForbidden, "/admin/login")
		return
	}
	c.HTML(http.StatusOK, "admin_dashboard.html", gin.H{})
}
