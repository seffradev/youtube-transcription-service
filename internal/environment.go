package internal

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

func Environment() (string, string, string, error) {
	var err error

	log.SetPrefix("[APP] ")

	err = godotenv.Load("configs/webserver/.env")
	if err != nil {
		return "", "", "", err
	}

	ip := os.Getenv("IP")
	port := os.Getenv("PORT")
    bootstrapServers := os.Getenv("BOOTSTRAP_SERVERS")

	return ip, port, bootstrapServers, err
}
