package cmd

import (
	"context"
	"log"
	"time"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/db"
	"github.com/elvinsavio/cb-website-v2/models"
	"github.com/urfave/cli/v2"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

var SetupCommand = &cli.Command{
	Name:  "setup",
	Usage: "Seed roles and create admin account",
	Flags: []cli.Flag{
		&cli.StringFlag{
			Name:     "email",
			Usage:    "Admin email address",
			Required: true,
		},
		&cli.StringFlag{
			Name:     "password",
			Usage:    "Admin password",
			Required: true,
		},
	},
	Action: func(c *cli.Context) error {
		db.Connect(config.MongoURI, config.DBName)

		ctx, cancel := context.WithTimeout(context.Background(), 15*time.Second)
		defer cancel()

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

		admin_role := models.Role{Name: "admin"}
		_, err = admin_role.New()

		if err != nil {
			log.Fatalf("Creating admin role failed: %v", err)
		}

		editor_role := models.Role{Name: "editor"}
		_, err = editor_role.New()

		if err != nil {
			log.Fatalf("Creating editor role failed: %v", err)
			return nil
		}

		admin_user := models.User{}

		_, err = admin_user.New(
			c.String("email"),
			c.String("password"),
			admin_role.ID,
		)

		if err != nil {
			log.Fatalf("Creating admin user failed: %v", err)
		}

		log.Println("Setup complete.")
		return nil
	},
}
