def build_notification(
        type: str,
        action: str,
        photo_id: int,
        initiator_username: str = 'Moderator',
        votes_count: int = None,
        comments_count: int = None
) -> dict:
    """
    Function to be called at "message" parameter of channel_layer.group_send()
    Forms a dictionary that is going to be sent to channel_layer group and then to the client
    'type' is needed to pass the consumer handler method
    """

    notification = {
        "type": type,
        "notification":{
            "action": action,
            "photo_id": photo_id,
            "initiator_username": initiator_username
        }
    }

    #naming stuff as always
    if votes_count is not None:
        notification['notification']['votes_amount'] = votes_count
    if comments_count is not None:
        notification['notification']['comments_amount'] = comments_count

    return notification
