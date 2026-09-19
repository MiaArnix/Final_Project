from django.apps import AppConfig

# import rules
class ApiConfig(AppConfig):
    name = 'api'
    
    def ready(self):
        import api.rules
