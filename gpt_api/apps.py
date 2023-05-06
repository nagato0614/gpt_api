from django.apps import AppConfig


class GptAPIConfig(AppConfig):
    """
    chatGPTを使用したAPI
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'gpt_api'
