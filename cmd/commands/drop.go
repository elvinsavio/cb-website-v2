package cmd

import (
	"context"
	"fmt"
	"log"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/db"
	"github.com/urfave/cli/v2"
	"go.mongodb.org/mongo-driver/bson"
)

var DropCommand = &cli.Command{
	Name:  "drop-all",
	Usage: "Drops all collections in the database",
	Action: func(c *cli.Context) error {
		db.Connect(config.MongoURI, config.DBName)

		collections, err := db.DB.ListCollectionNames(context.Background(), bson.D{})
		if err != nil {
			log.Fatalf("Failed to list collections: %v", err)
		}

		for _, collName := range collections {
			err := db.DB.Collection(collName).Drop(context.Background())
			if err != nil {
				log.Printf("Failed to drop collection %s: %v", collName, err)
			} else {
				log.Printf("Dropped collection: %s", collName)
			}
		}

		fmt.Println("All collections dropped.")
		return nil
	},
}
