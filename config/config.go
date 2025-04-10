package config

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

var (
	MongoURI  string
	DBName    string
	Port      string
	JwtSecret string
)

func Load() {
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found, using environment variables")
	}

	MongoURI = getEnv("MONGO_URI", "mongodb://localhost:27017")
	DBName = getEnv("DB_NAME", "cb_website")
	Port = getEnv("PORT", "8080")
	JwtSecret = getEnv("JWT_SECRET", "secret")

}

func getEnv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
