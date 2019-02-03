from django.core.management.base import BaseCommand
from assessment.seeders.base_seeder import Seeder
class Command(BaseCommand, Seeder):

    
    def handle(self, *args, **options):
        self.seed_all()
        print('Initial data added to the database')