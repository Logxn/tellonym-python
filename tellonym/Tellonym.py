import requests
import json
from tellonym.exceptions import *
from tellonym.User import User

class Tellonym:

    def __init__(self, username, password):
        """
        Initializes a new Tellonym Object

        Args:
            username (str): your username for Tellonym
            password (str): your password for Tellonym
        """
        self.base_url = 'https://api.tellonym.me'
        self.login_url = self.base_url + '/tokens/create'
        self.logout_url = self.base_url + '/tokens/destroy'
        self.get_user_url = self.base_url + '/accounts/myself'
        self.get_tells_url = self.base_url + '/tells'
        self.send_tells_url = self.base_url + '/tells/create'
        self.delete_tell_url = self.base_url + '/tells/destroy'
        self.non_auth_header = {'user-agent': 'Tellonym/180 CFNetwork/976 Darwin/18.2.0', 'tellonym-client':'ios:2.14.1'}
        self.auth = 'Bearer ' + self.get_request_token(username, password)
        self.auth_header = {'Authorization': self.auth, 'user-agent':'Tellonym/180 CFNetwork/976 Darwin/18.2.0', 'tellonym-client':'ios:2.14.1'}

    def get_request_token(self, username, password):
        """
        Used to login to Tellonym

        Args:
            password (str): your password for Tellonym

        Returns:
            req_token (str): the request token used for authenticating our requests
        """

        body = {
        'country': 'DE',
        'deviceName': 'tellonym-for-python',
        'deviceType': 'ios',
        'lang': 'de',
        'email': username,
        'password': password,
        'idfa': '',
        'limit': 13
        }

        r = requests.post(self.login_url, json=body, headers=self.non_auth_header)

        response = r.json()

        if 'err' in response:
            if response['err']['code']:
                raise WrongCredentialsError

        req_token = response['accessToken']
        self.req_token = req_token
        return req_token

    def logout(self):
        """
        Used to logout from Tellonym

        Returns:
            "Success": Logout succeeded
        """

        r = requests.post(self.logout_url, headers=self.auth_header)

        if r.status_code == 403:
            raise UnauthorizedError

        return 'Success'

    def get_user(self):
        """
        Fetches the own profile
        """

        r = requests.get(self.get_user_url, headers=self.auth_header)
        user = User(r.json())

        return user

    def get_tells(self):
        """
        Gets all Tells for the current user

        Returns:
            tells_array (array): all current tells for the user
        """

        r = requests.get(self.get_tells_url, headers=self.auth_header)
        tells = r.json()
        tells_array = []
        for index, _ in enumerate(tells['tells']):
            tells_array.append(tells['tells'][index])
        return tells_array

    def send_tell(self, id, text, anonymous=True):
        """
        Sends a Tell to a specific user

        Args:
            id (int): the id of the desired user
            text (str): text to send with the tell
            anonymous (bool): defines wether the tell is to be sent anonymously or not - defaults to true

        Returns:
            "Success": Tell sucessfully sent
        """

        if anonymous == False:
            body = {
            'senderStatus': 2,
            'previousRouteName': 'Result',
            'tell': text,
            'userId': id,
            'limit': 13
            }
        else:
            body = {
            'previousRouteName': 'Result',
            'tell': text,
            'userId': id,
            'limit': 13
            }

        r = requests.post(self.send_tells_url, json=body, headers=self.auth_header)
        response = r.json()

        if response == 'ok':
            return 'Success'
        elif response['err']['code'] == 'NOT_FOUND':
            raise UserNotFoundError
        else:
            raise UnknownError

    def delete_tell(self, id):
        """
        Deletes a specific Tell for the current user

        Args:
            id (int): the id of the tell to delete

        Returns:
            "Success": Tell deleted
        """

        body = {
        'tellId': id,
        'limit': 13
        }

        r = requests.post(self.delete_tell_url, json=body, headers=self.auth_header)

        # I tested everything from sending a string to a random number
        # there doesn't seem to be anything else but a OK (200) status code
        # or Unauthorized (403) if the token is not valid
        if r.status_code == 403:
            raise UnauthorizedError

        return 'Success'
