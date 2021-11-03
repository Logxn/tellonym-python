import requests
from tellonym.exceptions import *


class Answer:

    def __init__(self, client, input):
        self.__client = client
        self.type = input['type']
        self.id = input['id']
        self.content = input['answer']
        self.likes_count = input['likesCount']
        self.created_at = input['createdAt']
        self.tell = input['tell']
        self.sender_status = input['senderStatus']
        self.sender = input['sender']
        self.is_liked = input['isLiked']
        self.user_id = input['userId']
        self.is_current_user_tell_sender = input['isCurrentUserTellSender']
        self.likes = input['likes']  # to-do: put this in a seperate class (?)

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

    def like(self):
        """
        Likes the answer on the user's profile

        Returns:
            True (bool): Answers has been liked
            UnknownError (exception): UnknownError has occurred
        """
        body = {
            "answerId": self.id,
            "userId": self.recipient_id,
            "limit": 13
        }

        r = requests.post(self.__client.create_like_url, json=body, headers=self.__client.auth_header)

        if r.status_code == 200:
            return True
        raise UnknownError

    def delete(self):
        """
        Deletes the answer on the user's profile
        """

        body = {
            'answerId': self.id,
            'userId': self.recipient_id,
            'limit': 13
        }

        r = requests.post(self.__client.delete_answer_url, json=body, headers=self.__client.auth_header)

        if r.status_code == 200:
            return True
        raise UnknownError
