from django.contrib.auth.models import User


def seed_user():
    
    user_data = [
            User(username='kenware', is_superuser=True, is_staff=True, first_name='kevin', last_name='eze'),
            User(username='kennedy', is_staff=True, first_name='kenneth', last_name='eze'),
            User(username='emeka', first_name='emeke', last_name='eze'),
            
       ]

    for user in user_data:
        username = user.username
        if not User.objects.filter(username=username):
            user.save()
            user = User.objects.get(username=username)
            password = user.username
            user.set_password(password)
            user.save()
            print(f'user with password {user.username} successfuly seeded >>>>>>')