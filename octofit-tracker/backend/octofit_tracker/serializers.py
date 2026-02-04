from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout
from bson import ObjectId


class UserSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['_id', 'name', 'email', 'team_id', 'created_at']
    
    def get__id(self, obj):
        return str(obj._id)


class TeamSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = ['_id', 'name', 'description', 'created_at']
    
    def get__id(self, obj):
        return str(obj._id)


class ActivitySerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['_id', 'user_id', 'activity_type', 'duration', 'calories', 'date', 'created_at']
    
    def get__id(self, obj):
        return str(obj._id)


class LeaderboardSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = Leaderboard
        fields = ['_id', 'user_id', 'team_id', 'total_calories', 'total_duration', 'rank', 'updated_at']
    
    def get__id(self, obj):
        return str(obj._id)


class WorkoutSerializer(serializers.ModelSerializer):
    _id = serializers.SerializerMethodField()
    
    class Meta:
        model = Workout
        fields = ['_id', 'name', 'description', 'activity_type', 'difficulty', 'estimated_calories', 'estimated_duration']
    
    def get__id(self, obj):
        return str(obj._id)
