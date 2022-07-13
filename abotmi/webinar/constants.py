from django.conf import settings
# Webinar API KEY
WEBINAR_API_KEY = None

if settings.WEBINAR_API_KEY:
    WEBINAR_API_KEY = settings.WEBINAR_API_KEY
else:
    WEBINAR_API_KEY = "APP_KEY"

# SET Validation Message
NAME_VALIDATION_MESSAGE = "Please enter room name !"
LOBBY_VALIDATION_MESSAGE = "Please enter lobby description !"
STARTS_AT_VALIDATION_MESSAGE = "Please schedule the meeting date and time !"
DURATION_VALIDATION_MESSAGE = "Please provide duration between 5 minutes and 3 hours !"