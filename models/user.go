package models

import "go.mongodb.org/mongo-driver/bson/primitive"

type User struct {
	Email    string             `bson:"email"`
	Password string             `bson:"password"` // hashed
	Role     primitive.ObjectID `bson:"role"`
}
