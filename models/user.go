package models

import (
	"context"

	"github.com/elvinsavio/cb-website-v2/db"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
	"golang.org/x/crypto/bcrypt"
)

type User struct {
	ID       primitive.ObjectID `bson:"_id,omitempty"`
	Email    string             `bson:"email"`
	Password []byte             `bson:"password"` // hashed
	Role     primitive.ObjectID `bson:"role"`
}

func (u *User) New(email string, password string, role primitive.ObjectID) (*User, error) {

	collection := db.DB.Collection("users")
	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(password), bcrypt.DefaultCost)

	if err != nil {
		return nil, err
	}

	u.Email = email
	u.Password = hashedPassword
	u.Role = role

	_admin, err := collection.InsertOne(context.Background(), u)

	if err != nil {
		return nil, err
	}

	admin := _admin.InsertedID.(primitive.ObjectID)
	u.ID = admin

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
