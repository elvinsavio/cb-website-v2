package main

import (
	"github.com/elvinsavio/cb-website-v2/routes"
	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()
	r.Static("/static", "./static")

	r.LoadHTMLGlob("templates/**/*")

	// Client-facing routes
	routes.RegisterClientRoutes(r)

	// Admin routes
	routes.RegisterAdminRoutes(r)

	r.Run(":8080")
}
