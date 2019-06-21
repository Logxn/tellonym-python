import json

class Answer:

    def __init__(self, input):
        self.id = input['id']
        self.answer = input['answer']
        self.likes_count= input['likesCount']
        self.created_at = input['createdAt']
        self.tell = input['tell']
        self.sender_status = input['senderStatus']
        self.sender = input['sender']
        self.recipient_id = input['userId']
        self.is_current_user_tell_sender = input['isCurrentUserTellSender']
        self.likes = input['likes'] # to-do: put this in a seperate class (?)

    def is_anonymous_tell(self):
        """
        Checks wether or not the tell was received by an anonymous person
        0: Anonymous
        1: Unknown
        2: Public Sender

        Returns:
            True: The tell was received by an anonymous person
            False: The tell was received by a public sender
        """
        if self.sender_status == 0:
            return True
        return False
