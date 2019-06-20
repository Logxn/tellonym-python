import requests
import json

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

        req_token = r.json()['accessToken']
        self.req_token = req_token
        return req_token

    def logout(self):
        """
        Used to logout from Tellonym

        Returns:
            True: Logout succeeded
        """

        r = requests.post(self.logout_url, headers=self.auth_header)

        if r.status_code == 403:
            raise UnauthorizedError

        return True

    def delete_tell(self, id):
        """
        Used to delete a Tell that has been received

        Args:
            id (int): the id of the tell to delete
        """

        body = {
        "tellId": id,
        "limit": 13
        }

        r = requests.post(self.delete_tell_url, json=body, headers=self.auth_header)

        # I tested everything from sending a string to a random number
        # there doesn't seem to be anything else but a OK (200) status code
        # or Unauthorized (403) if the token is not valid
        if r.status_code == 403:
            raise UnauthorizedError
