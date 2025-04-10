package handlers

import (
	"log"
	"net/http"
	"time"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/models"
	"github.com/golang-jwt/jwt/v5"
	"golang.org/x/crypto/bcrypt"

	"github.com/gin-gonic/gin"
)

var jwtSecret = []byte(config.JwtSecret)

func RenderLoginPage(c *gin.Context) {
	c.HTML(http.StatusOK, "login_page", gin.H{})
}

func RenderAdminDashboard(c *gin.Context) {
	c.HTML(http.StatusOK, "dashboard_page", gin.H{})
}

func HandleLogin(c *gin.Context) {
	log.Println("Handling login")
	username := c.PostForm("username")
	// password := c.PostForm("password")

	user := &models.User{}
	user, err := user.FindUser(username)
	log.Println(user)
	if err != nil {
		c.HTML(http.StatusUnauthorized, "partials/login_form.html", gin.H{
			"Error": "Invalid credentials",
		})
		return
	}

	password := []byte(c.PostForm("password"))
	err = bcrypt.CompareHashAndPassword(user.Password, password)
	if err != nil {
		c.HTML(http.StatusUnauthorized, "partials/login_form.html", gin.H{
			"Error": "Invalid credentials",
		})
		return
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"username": username,
		"exp":      time.Now().Add(time.Hour * 24 * 7).Unix(),
	})

	tokenString, err := token.SignedString(jwtSecret)

	if err != nil {
		log.Println("Error generating JWT token:", err)
		return
	}

	c.SetCookie("session", tokenString, int(time.Hour*24*7), "/", "", false, true)

	// send ok
	c.Header("HX-Redirect", "/admin/")
	c.Status(http.StatusOK)
}
