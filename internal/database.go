package internal

import (
    "gorm.io/driver/mysql"
    "gorm.io/gorm"
)

func Database(db_url string) (*gorm.DB, error) {
    var err error

    db, err := gorm.Open(mysql.Open(db_url), &gorm.Config{})
    if err != nil {
        return nil, err
    }

    return db, err
}
