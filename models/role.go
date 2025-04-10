package models

import (
	"context"

	"github.com/elvinsavio/cb-website-v2/db"
	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/bson/primitive"
)

type Role struct {
	ID   primitive.ObjectID `bson:"_id,omitempty"`
	Name string             `bson:"name"`
}

func (r *Role) New() (*Role, error) {
	collection := db.DB.Collection("roles")
	_, err := collection.InsertOne(context.Background(), r)
	if err != nil {
		return nil, err
	}
	return r, nil
}

func (r *Role) FindName(name string) (*Role, error) {
	collection := db.DB.Collection("roles")
	filter := bson.M{"name": name}
	var role Role
	err := collection.FindOne(context.Background(), filter).Decode(&role)
	if err != nil {
		return nil, err
	}
	return &role, nil
}

func (r *Role) FindID(id primitive.ObjectID) (*Role, error) {
	collection := db.DB.Collection("roles")
	filter := bson.M{"_id": id}
	var role Role
	err := collection.FindOne(context.Background(), filter).Decode(&role)
	if err != nil {
		return nil, err
	}
	return &role, nil
}
