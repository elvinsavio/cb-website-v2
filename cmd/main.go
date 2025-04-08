package main

import (
	"log"
	"os"

	cmd "github.com/elvinsavio/cb-website-v2/cmd/commands"
	"github.com/elvinsavio/cb-website-v2/config"
	"github.com/urfave/cli/v2"
)

func main() {
	config.Load()
	app := &cli.App{
		Name:  "classic-bikes",
		Usage: "Database setup / teardown",
		Commands: []*cli.Command{
			cmd.SetupCommand,
			cmd.DropCommand,
		},
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}
