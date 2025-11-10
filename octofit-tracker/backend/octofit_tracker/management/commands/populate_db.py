from django.core.management.base import BaseCommand
from django.conf import settings
from djongo import models
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation and raw operations
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Drop collections if they exist
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create unique index on email for users
        db.users.create_index([('email', 1)], unique=True)

        # Sample data
        users = [
            {"name": "Tony Stark", "email": "tony@marvel.com", "team": "marvel"},
            {"name": "Steve Rogers", "email": "steve@marvel.com", "team": "marvel"},
            {"name": "Bruce Wayne", "email": "bruce@dc.com", "team": "dc"},
            {"name": "Clark Kent", "email": "clark@dc.com", "team": "dc"},
        ]
        teams = [
            {"name": "marvel", "members": ["tony@marvel.com", "steve@marvel.com"]},
            {"name": "dc", "members": ["bruce@dc.com", "clark@dc.com"]},
        ]
        activities = [
            {"user_email": "tony@marvel.com", "activity": "Run", "distance": 5},
            {"user_email": "steve@marvel.com", "activity": "Swim", "distance": 2},
            {"user_email": "bruce@dc.com", "activity": "Bike", "distance": 10},
            {"user_email": "clark@dc.com", "activity": "Fly", "distance": 100},
        ]
        leaderboard = [
            {"team": "marvel", "points": 150},
            {"team": "dc", "points": 200},
        ]
        workouts = [
            {"name": "Super Strength", "suggested_for": ["marvel", "dc"]},
            {"name": "Flight Training", "suggested_for": ["dc"]},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
