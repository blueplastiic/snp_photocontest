from service_objects.services import Service

class UpdatePublicUserInfoService(Service):
    def process(self): #pyright: ignore
        user = self.data.get('user')
        if not user:
            raise ValueError('User cannot be found')

        username = self.data.get('username')
        about = self.data.get('about')
        if not username and not about:
            raise ValueError('Data not provided')

        if username:
            user.username = username
        if about:
            user.about = about

        user.save()

