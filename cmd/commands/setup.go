package cmd

import (
	"bufio"
	"context"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/db"
	"github.com/elvinsavio/cb-website-v2/models"
	"github.com/urfave/cli/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"golang.org/x/crypto/bcrypt"
)

var SetupCommand = &cli.Command{
	Name:  "setup",
	Usage: "Seed roles and create admin account",
	Action: func(c *cli.Context) error {
		db.Connect(config.MongoURI, config.DBName)

		ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()

		roles := []interface{}{
			models.Role{Name: "admin"},
			models.Role{Name: "editor"},
		}

		_, err := db.DB.Collection("roles").Indexes().CreateOne(ctx, mongo.IndexModel{
			Keys:    bson.D{{Key: "name", Value: 1}},
			Options: options.Index().SetUnique(true),
		})
		if err != nil {
			log.Fatalf("Creating index on roles failed: %v", err)
		}

		_, err = db.DB.Collection("users").Indexes().CreateOne(ctx, mongo.IndexModel{
			Keys:    bson.D{{Key: "email", Value: 1}},
			Options: options.Index().SetUnique(true),
		})
		if err != nil {
			log.Fatalf("Creating index on users failed: %v", err)
		}

		_, err = db.DB.Collection("roles").InsertMany(ctx, roles)
		if err != nil {
			log.Fatalf("Inserting roles failed: %v", err)
		}

		reader := bufio.NewReader(os.Stdin)

		fmt.Print("Admin email: ")
		email, _ := reader.ReadString('\n')
		email = strings.TrimSpace(email)

		fmt.Print("Admin password: ")
		password, _ := reader.ReadString('\n')
		password = strings.TrimSpace(password)

		hash, _ := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

		var adminRole bson.M
		err = db.DB.Collection("roles").FindOne(ctx, bson.M{"name": "admin"}).Decode(&adminRole)
		if err != nil {
			log.Fatalf("Fetching admin role failed: %v", err)
		}

		admin := models.User{
			Email:    email,
			Password: string(hash),
			Role:     adminRole["_id"].(primitive.ObjectID),
		}

		_, err = db.DB.Collection("users").InsertOne(ctx, admin)
		if err != nil {
			log.Fatalf("Creating admin user failed: %v", err)
		}

		fmt.Println("✅ Setup complete.")
		return nil
	},
}
