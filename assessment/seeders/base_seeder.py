
from .seed_assessment import seed_assessment
from .seed_question import seed_question
from .seed_answer import seed_answer
from .seed_user import seed_user
from .seed_score import seed_score

class Seeder(object):
   
   def seed_all(self):
       seed_assessment()
       seed_question()
       seed_answer()
       seed_user()
       seed_score()
