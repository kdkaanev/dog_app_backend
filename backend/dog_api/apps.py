from django.apps import AppConfig


class DogApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend.dog_api'



    def ready(self):
        pass