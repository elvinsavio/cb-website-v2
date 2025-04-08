package main

import (
	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/routes"
	"github.com/gin-gonic/gin"
)

func main() {
	config.Load()

	r := gin.Default()
	r.Static("/static", "./static")

	r.LoadHTMLGlob("templates/**/*")

	// Client-facing routes
	routes.RegisterClientRoutes(r)

	// Admin routes
	routes.RegisterAdminRoutes(r)

	r.Run(":" + config.Port)
}
