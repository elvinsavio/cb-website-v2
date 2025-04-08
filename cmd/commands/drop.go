package cmd

import (
	"context"
	"fmt"
	"log"

	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/elvinsavio/cb-website-v2/db"
	"github.com/urfave/cli/v2"
)

var DropCommand = &cli.Command{
	Name:  "drop-all",
	Usage: "Deletes the entire database",
	Action: func(c *cli.Context) error {
		db.Connect(config.MongoURI, config.DBName)

		err := db.DB.Drop(context.Background())
		if err != nil {
			log.Fatalf("Drop failed: %v", err)
		}

		fmt.Println("🗑️ All data deleted.")
		return nil
	},
}
