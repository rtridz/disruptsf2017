import datetime
from facebook import GraphAPI

from core import models


class FacebookBackend:
    def authenticate(self, token=None, expires=None):

        facebook_session = models.FacebookSession.objects.get_or_create(
            access_token=token,
        )[0]

        facebook_session.expires = expires
        facebook_session.save()

        graph = GraphAPI(access_token=token, timeout=expires)
        args = {'fields': 'id,name,email,birthday,gender,link'}
        profile = graph.get_object('me', **args)

        print(profile)

        try:
            user = models.MyUser.objects.get(username=profile['id'])
        except models.MyUser.DoesNotExist as e:

            facebook_id = profile.get('id')
            username = facebook_id
            email = profile.get('email')
            name = profile.get('name')
            birthday = profile.get('birthday')
            birthday = datetime.datetime.strptime(birthday, '%d/%m/%Y').strftime('%Y-%m-%d')
            gender = profile.get('gender')
            link = profile.get('link')
            user = models.MyUser.objects.create_user(email=email, date_of_birth=birthday, password=facebook_id,
                                              facebook_id=facebook_id, link=link, name=name, gender=gender,
                                              username=username)




        try:
            models.FacebookSession.objects.get(uid=profile['id']).delete()
        except models.FacebookSession.DoesNotExist as e:
            pass

        facebook_session.uid = profile['id']
        facebook_session.user = user
        facebook_session.save()

        return user

    def get_user(self, user_id):

        try:
            return models.MyUser.objects.get(pk=user_id)
        except models.MyUser.User.DoesNotExist:
            return None