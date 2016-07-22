from django.apps import AppConfig


class DiscussionConfig(AppConfig):
    name = 'discussion'
    verbose_name = 'Django Discussion'

    def ready(self):
        import discussion.signals
