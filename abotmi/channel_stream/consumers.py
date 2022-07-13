import json
import logging
from channels import Channel, Group
from channels.auth import channel_session_user_from_http, channel_session_user
logger = logging.getLogger(__name__)

# This decorator copies the user from the HTTP session (only available in
# websocket.connect or http.request messages) to the channel session (available
# in all consumers with the same reply_channel, so all three here)


@channel_session_user_from_http
def ws_connect(message):
    message.reply_channel.send({'accept': True})
    # Initialise their session
    message.channel_session['rooms'] = []
    message.channel_session['rooms']

# Unpacks the JSON in the received WebSocket frame and puts it onto a channel
# of its own with a few attributes extra so we can route it
# This doesn't need @channel_session_user as the next consumer will have that,
# and we preserve message.reply_channel (which that's based on)


def ws_receive(message):
    # All WebSocket frames have either a text or binary payload; we decode the
    # text part here assuming it's JSON.
    # You could easily build up a basic framework that did this encoding/decoding
    # for you as well as handling common errors.
    payload = json.loads(message['text'])
    payload['reply_channel'] = message.content['reply_channel']
    Channel("trex.receive").send(payload)

@channel_session_user
def ws_disconnect(message):
    # Unsubscribe from any connected rooms
    #this is just debugg statement
    logger.info("Inside disconnect method")
    Group("room-%s" % 1).discard(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({"data": "I am inside ws_disconnect method"}),
    })

### Chat channel handling ###
# Channel_session_user loads the user out from the channel session and presents
# it as message.user. There's also a http_session_user if you want to do this on
# a low-level HTTP handler, or just channel_session if all you want is the
# message.channel_session object without the auth fetching overhead.


@channel_session_user
def trex_join(message):
    Group("room-%s" % 1).add(message.reply_channel)
    message.reply_channel.send({
        "text": json.dumps({
            "join": str(1),
            "title": "AbotmiRoom",
        }),
    })


@channel_session_user
def trex_leave(message):
    # Send a message back that will prompt them to close the room
    message.reply_channel.send({
        "text": json.dumps({
            "leave": str(1),
        }),
    })


@channel_session_user
def trex_send(message):
    final_msg = message.content
    print(final_msg, "===============final_msg")
    # type = final_msg.get("type", None)
    # if type == "reingo_bought_from_developer" or type == "reingo_bought_from_trading":
    #     urmView = UserReingoMapViewSet()
    #     reingo_id = final_msg.get("reingo_id",None)
    #     if reingo_id:
    #         data, status, project_card_details = urmView.get_websocket_trading_record_after_booking(
    #             reingo_id, type)
    #         if status:
    #             final_msg['traded_reingo_data'] = data
    #         if project_card_details:
    #             final_msg['project_card_details'] = project_card_details
    Group("room-%s" % 1).send(
        {"text": json.dumps(final_msg)}
    )