package internal

import (
	"log"
	"os"

	"github.com/joho/godotenv"
)

func Environment() (string, string, error) {
	var err error

	log.SetPrefix("[APP] ")

	err = godotenv.Load("configs/.env")
	if err != nil {
		return "", "", err
	}

	ip := os.Getenv("IP")
	port := os.Getenv("PORT")

	return ip, port, err
}
