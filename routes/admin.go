package routes

import (
	"github.com/elvinsavio/cb-website-v2/handlers"
	"github.com/elvinsavio/cb-website-v2/middleware"
	"github.com/gin-gonic/gin"
)

func RegisterAdminRoutes(r *gin.Engine) {
	admin := r.Group("/admin")
	admin.GET("login", handlers.RenderLoginPage)
	admin.POST("/login", handlers.HandleLogin)
	admin.GET("/", middleware.AuthMiddleware(), handlers.RenderAdminDashboard)

}
