from djongo import models
from bson import ObjectId


class User(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    team_id = models.CharField(max_length=24, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.name


class Team(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return self.name


class Activity(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user_id = models.CharField(max_length=24)
    activity_type = models.CharField(max_length=100)
    duration = models.IntegerField()  # in minutes
    calories = models.IntegerField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'activities'
    
    def __str__(self):
        return f"{self.activity_type} - {self.duration} mins"


class Leaderboard(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    user_id = models.CharField(max_length=24)
    team_id = models.CharField(max_length=24)
    total_calories = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0)  # in minutes
    rank = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'leaderboard'
    
    def __str__(self):
        return f"Rank {self.rank} - User {self.user_id}"


class Workout(models.Model):
    _id = models.ObjectIdField(primary_key=True, default=ObjectId)
    name = models.CharField(max_length=200)
    description = models.TextField()
    activity_type = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    estimated_calories = models.IntegerField()
    estimated_duration = models.IntegerField()  # in minutes
    
    class Meta:
        db_table = 'workouts'
    
    def __str__(self):
        return self.name
