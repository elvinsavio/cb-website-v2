package handlers

import (
	"log"
	"net/http"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/models"

	"github.com/gin-gonic/gin"
)

var jwtSecret = config.JwtSecret

func RenderLoginPage(c *gin.Context) {
	c.HTML(http.StatusOK, "login_page", gin.H{})
}

func RenderAdminDashboard(c *gin.Context) {
	c.HTML(http.StatusOK, "admin_dashboard.html", gin.H{})
}

func HandleLogin(c *gin.Context) {
	log.Println("Handling login")
	username := c.PostForm("username")
	// password := c.PostForm("password")

	user := &models.User{}
	_, err := user.FindUser(username)

	if err != nil {
		c.HTML(http.StatusUnauthorized, "partials/login_form.html", gin.H{
			"Error": "Invalid credentials",
		})
		return
	}
	// send ok
	c.JSON(http.StatusOK, gin.H{
		"message": "ok",
		"user":    user,
	})
}
