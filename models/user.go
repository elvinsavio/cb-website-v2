package models

import (
	"context"

	"github.com/elvinsavio/cb-website-v2/db"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type User struct {
	ID       primitive.ObjectID `bson:"_id,omitempty"`
	Email    string             `bson:"email"`
	Password string             `bson:"password"` // hashed
	Role     primitive.ObjectID `bson:"role"`
}

func (u *User) New() (*User, error) {
	collection := db.DB.Collection("users")
	_, err := collection.InsertOne(context.Background(), u)

	if err != nil {
		return nil, err
	}

	return u, nil

}
