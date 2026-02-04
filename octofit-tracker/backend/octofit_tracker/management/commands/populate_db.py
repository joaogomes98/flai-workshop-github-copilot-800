from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from datetime import datetime, timedelta
from bson import ObjectId
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))
        
        # Delete existing data
        self.stdout.write('Deleting existing data...')
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()
        
        # Create Teams
        self.stdout.write('Creating teams...')
        team_marvel = Team.objects.create(
            name='Team Marvel',
            description='Earths Mightiest Heroes united to protect the world'
        )
        
        team_dc = Team.objects.create(
            name='Team DC',
            description='Justice League - Defenders of truth and justice'
        )
        
        # Create Users (Superheroes)
        self.stdout.write('Creating superhero users...')
        marvel_heroes = [
            {'name': 'Iron Man', 'email': 'tony.stark@marvel.com'},
            {'name': 'Captain America', 'email': 'steve.rogers@marvel.com'},
            {'name': 'Thor', 'email': 'thor.odinson@marvel.com'},
            {'name': 'Hulk', 'email': 'bruce.banner@marvel.com'},
            {'name': 'Black Widow', 'email': 'natasha.romanoff@marvel.com'},
            {'name': 'Spider-Man', 'email': 'peter.parker@marvel.com'},
        ]
        
        dc_heroes = [
            {'name': 'Superman', 'email': 'clark.kent@dc.com'},
            {'name': 'Batman', 'email': 'bruce.wayne@dc.com'},
            {'name': 'Wonder Woman', 'email': 'diana.prince@dc.com'},
            {'name': 'The Flash', 'email': 'barry.allen@dc.com'},
            {'name': 'Aquaman', 'email': 'arthur.curry@dc.com'},
            {'name': 'Green Lantern', 'email': 'hal.jordan@dc.com'},
        ]
        
        marvel_users = []
        for hero in marvel_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_marvel._id)
            )
            marvel_users.append(user)
        
        dc_users = []
        for hero in dc_heroes:
            user = User.objects.create(
                name=hero['name'],
                email=hero['email'],
                team_id=str(team_dc._id)
            )
            dc_users.append(user)
        
        all_users = marvel_users + dc_users
        
        # Create Activities
        self.stdout.write('Creating activities...')
        activity_types = [
            {'type': 'Running', 'cal_per_min': 10},
            {'type': 'Weight Training', 'cal_per_min': 8},
            {'type': 'Swimming', 'cal_per_min': 12},
            {'type': 'Cycling', 'cal_per_min': 9},
            {'type': 'Combat Training', 'cal_per_min': 15},
            {'type': 'Yoga', 'cal_per_min': 5},
        ]
        
        for user in all_users:
            # Create 10 random activities for each user
            for i in range(10):
                activity = random.choice(activity_types)
                duration = random.randint(30, 120)
                calories = duration * activity['cal_per_min']
                date = datetime.now() - timedelta(days=random.randint(0, 30))
                
                Activity.objects.create(
                    user_id=str(user._id),
                    activity_type=activity['type'],
                    duration=duration,
                    calories=calories,
                    date=date
                )
        
        # Create Leaderboard entries
        self.stdout.write('Creating leaderboard entries...')
        leaderboard_data = []
        
        for user in all_users:
            activities = Activity.objects.filter(user_id=str(user._id))
            total_calories = sum(a.calories for a in activities)
            total_duration = sum(a.duration for a in activities)
            
            leaderboard_data.append({
                'user': user,
                'total_calories': total_calories,
                'total_duration': total_duration
            })
        
        # Sort by total calories and assign ranks
        leaderboard_data.sort(key=lambda x: x['total_calories'], reverse=True)
        
        for rank, entry in enumerate(leaderboard_data, start=1):
            Leaderboard.objects.create(
                user_id=str(entry['user']._id),
                team_id=entry['user'].team_id,
                total_calories=entry['total_calories'],
                total_duration=entry['total_duration'],
                rank=rank
            )
        
        # Create Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Stark Industries Power Workout',
                'description': 'High-intensity training inspired by Iron Mans suit technology',
                'activity_type': 'Weight Training',
                'difficulty': 'Advanced',
                'estimated_calories': 500,
                'estimated_duration': 60
            },
            {
                'name': 'Asgardian Thunder Run',
                'description': 'Endurance running worthy of Thor himself',
                'activity_type': 'Running',
                'difficulty': 'Intermediate',
                'estimated_calories': 600,
                'estimated_duration': 60
            },
            {
                'name': 'Batcave Circuit Training',
                'description': 'Comprehensive workout from Batmans training regimen',
                'activity_type': 'Combat Training',
                'difficulty': 'Advanced',
                'estimated_calories': 700,
                'estimated_duration': 75
            },
            {
                'name': 'Amazonian Warrior Yoga',
                'description': 'Balance and flexibility training from Themyscira',
                'activity_type': 'Yoga',
                'difficulty': 'Beginner',
                'estimated_calories': 250,
                'estimated_duration': 50
            },
            {
                'name': 'Speedster Sprint Training',
                'description': 'High-velocity running drills inspired by The Flash',
                'activity_type': 'Running',
                'difficulty': 'Advanced',
                'estimated_calories': 800,
                'estimated_duration': 45
            },
            {
                'name': 'Atlantean Aqua Fitness',
                'description': 'Swimming workout from the depths of Atlantis',
                'activity_type': 'Swimming',
                'difficulty': 'Intermediate',
                'estimated_calories': 650,
                'estimated_duration': 55
            },
            {
                'name': 'Super Soldier Conditioning',
                'description': 'Captain Americas complete conditioning program',
                'activity_type': 'Weight Training',
                'difficulty': 'Advanced',
                'estimated_calories': 550,
                'estimated_duration': 70
            },
            {
                'name': 'Web-Slinger Agility Course',
                'description': 'Agility and flexibility training from Spider-Man',
                'activity_type': 'Combat Training',
                'difficulty': 'Intermediate',
                'estimated_calories': 450,
                'estimated_duration': 50
            },
        ]
        
        for workout_data in workouts:
            Workout.objects.create(**workout_data)
        
        # Print summary
        self.stdout.write(self.style.SUCCESS('\n=== Database Population Complete ==='))
        self.stdout.write(f'Teams created: {Team.objects.count()}')
        self.stdout.write(f'Users created: {User.objects.count()}')
        self.stdout.write(f'Activities created: {Activity.objects.count()}')
        self.stdout.write(f'Leaderboard entries: {Leaderboard.objects.count()}')
        self.stdout.write(f'Workouts created: {Workout.objects.count()}')
        self.stdout.write(self.style.SUCCESS('\nDatabase successfully populated with superhero data!'))
