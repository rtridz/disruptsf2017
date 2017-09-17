import datetime
from django.contrib.auth import models as auth_models
from core import models


class FacebookBackend:
    def authenticate(self, token=None):

        facebook_session = models.FacebookSession.objects.get(
            access_token=token,
        )

        profile = facebook_session.query('me')
        facebook_id = profile.get('id')
        username = profile.get('username')
        email = profile.get('email')
        name = profile.get('name')
        birthday = profile.get('birthday')
        birthday = datetime.datetime.strptime(birthday, '%m/%d/%Y').strftime('%Y-%m-%d')
        gender = profile.get('gender')
        link = profile.get('link')
        try:
            user = models.MyUser.objects.get(username=profile['id'])
        except auth_models.User.DoesNotExist as e:
            models.MyUser.objects.create_user(email=email, date_of_birth=birthday, password=facebook_id,
                                                  facebook_id=facebook_id, link=link, name=name, gender=gender,
                                                  username=username)

        user.set_unusable_password()

        user.save()

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
            return auth_models.User.objects.get(pk=user_id)
        except auth_models.User.DoesNotExist:
            return None

    # def facebookReturn(request):
    #     code = request.GET.get('code')
    #
    #     site = urlopen("https://graph.facebook.com/oauth/access_token?client_id=" + str(
    #         conf.facevook_id) + "&redirect_uri=http://localhost:8000/facebookreturn&client_secret=" + str(
    #         conf.facevook_id) + "&code=%s#_=_" % code)
    #
    #     site = site.replace("access_token=", '')
    #     m = site.find('&expires=')
    #     site = site[0:m]
    #
    #     ##this is the API call that uses the facebook module to get the user data
    #     graph = GraphAPI(site)
    #
    #     try:
    #         ##this checks if the user is registered on the system, if so it authenticates the user, if not it creates the user
    #         user = MyUser.objects.get(email=email)
    #         user = authenticate(username=email, password=facebook_id)
    #         return HttpResponse('this users email address is %s' % user)
    #     except ObjectDoesNotExist:
    #         New_user = MyUser.objects.create_user(email=email, date_of_birth=birthday, password=facebook_id,
    #                                               facebook_id=facebook_id, link=link, name=name, gender=gender,
    #                                               username=username)
    #         return HttpResponse(
    #             "facebook id %s\n, username %s\n, email %s\n, name %s\n, birthday %s\n, gender %s\n, link %s" % (
    #                 facebook_id, username, email, name, birthday, gender, link))




