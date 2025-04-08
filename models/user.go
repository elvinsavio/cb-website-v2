package models

type User struct {
	Email    string `bson:"email"`
	Password string `bson:"password"` // hashed
	Role     string `bson:"role"`
}
