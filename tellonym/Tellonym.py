import requests
from tellonym.exceptions import *
from tellonym.Profile import Profile
from tellonym.Tell import Tell
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
        self.create_like_url = self.base_url + '/likes/create'
        self.create_answer_url = self.base_url + '/answers/create'
        self.delete_answer_url = self.base_url + '/answers/destroy'
        self.search_user_url = self.base_url + '/search/users'
        self.non_auth_header = {'user-agent': 'Tellonym/180 CFNetwork/976 Darwin/18.2.0',
                                'tellonym-client': 'ios:2.14.1'}
        self.auth = 'Bearer ' + self.__get_request_token(username, password)
        self.auth_header = {'Authorization': self.auth, 'user-agent': 'Tellonym/180 CFNetwork/976 Darwin/18.2.0',
                            'tellonym-client': 'ios:2.14.1'}

    def __get_request_token(self, username, password):
        """
        Used to login to Tellonym

        Args:
            username (str): your username for Tellonym
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
            if response['err']['code'] == 'WRONG_CREDENTIALS':
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

    def get_profile(self):
        """
        Fetches the own profile

        Returns:
            Profile (class): Returns profile object with all the current user's information
        """

        r = requests.get(self.get_user_url, headers=self.auth_header)

        if r.status_code != 200:
            raise UnknownError

        profile = Profile(self, r.json())
        return profile

    def get_user(self, username, exact_match=False, case_sensitive=False):
        """
        Tries to fetch a user by its given name

        Args:
            username (str): the username to search for
            exact_match (bool): only return a user if the given name matches one of the results (defaults to false)
            case_sensitive (bool): only search for the name in case sensitive (defaults to false)
        """

        payload = {'searchString': username, 'term': username, 'limit': '13'}
        r = requests.get(self.search_user_url, params=payload, headers=self.auth_header)

        results = r.json()['results']

        if exact_match:
            for index, _ in enumerate(results):
                if case_sensitive:
                    if username in results[index]['username']:
                        return User(results[index])
                else:
                    if username in results[index]['username'] or username in results[index]['username'].lower():
                        return User(results[index])

        return "USER_NOT_FOUND"

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
            tell = Tell(self, tells['tells'][index])
            tells_array.append(tell)
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

        if not anonymous:
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
        elif response['err']['code'] == "PARAMETER_INVALID":
            raise InvalidParameterError
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

    def answer_tell(self, id, answer):

        """
            Answers a specific Tell for the current user

            Args:
                id (int): the id of the tell to answer
                answer (str): text to send as the answer

            Returns:
                "Success": Tell answered
        """
        body = {
            'answer': answer,
            'tellId': id,
            'limit': 13
        }

        r = requests.post(self.create_answer_url, json=body, headers=self.auth_header)

        response = r.json()

        if r.status_code == 200:
            return response
        elif response['err']['code'] == 'NOT_FOUND':
            raise TellNotFoundError
        elif response['err']['code'] == "PARAMETER_INVALID":
            raise InvalidParameterError
        elif response['err']['code'] == 'TOKEN_INVALID':
            raise UnauthorizedError
        else:
            raise UnknownError
