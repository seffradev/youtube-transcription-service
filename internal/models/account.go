package models

import (
    "gorm.io/gorm"
)

type Account struct {
    gorm.Model
	ID        int    `json:"id"`
	Name      string `json:"name"`
	Email     string `json:"email"`
	Password  string `json:"password"`
	AuthToken string `json:"auth_token"`
	Tokens    int    `json:"tokens"`
}
