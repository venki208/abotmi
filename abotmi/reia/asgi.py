import os
import channels
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reia.[SETTINGS]")
channel_layer = channels.asgi.get_channel_layer()
