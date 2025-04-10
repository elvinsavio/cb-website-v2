package models

import (
	"context"

	"github.com/elvinsavio/cb-website-v2/db"
	"go.mongodb.org/mongo-driver/bson"
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

func (u *User) FindUser(email string) (*User, error) {
	collection := db.DB.Collection("users")
	filter := bson.M{"email": email}
	var user User
	err := collection.FindOne(context.Background(), filter).Decode(&user)
	if err != nil {
		return nil, err
	}
	return &user, nil
}
