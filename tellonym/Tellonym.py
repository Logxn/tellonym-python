import requests
from tellonym.exceptions import *
from tellonym.Profile import Profile
from tellonym.Tell import Tell
from tellonym.User import User
#from 2captcha import 2Captcha
#import solver = 2Captch('d7fdaa6bcb831dcf1ff777f230192aff')


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
        self.delete_tell_url = self.base_url + '/posts/'
        self.create_like_url = self.base_url + '/likes/create'
        self.create_answer_url = self.base_url + '/answers/create'
        self.delete_answer_url = self.base_url + '/answers/destroy'
        self.search_user_url = self.base_url + '/search/users'
        self.non_auth_header = {'tellonym-client': 'ios:2.81.6:764:15:iPhone10,6', 'User-Agent': 'Tellonym/764 CFNetwork/1312 Darwin/21.0.0'}
        self.auth = 'Bearer ' + self.__get_request_token(username, password)
        self.auth_header = {'Authorization': self.auth, 'user-agent': 'Tellonym/737 CFNetwork/1240.0.4 Darwin/20.6.0',
                            'tellonym-client': 'ios:2.81.1:737:14:iPhone10,6'}
        self.captcha_key = '8623e8b4-d93c-40b4-9fb8-6ed629540b02'

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
            'deviceLanguage': 1,
            'deviceName': 'tell4pyt',
            'deviceType': 'ios',
            'deviceUid': '4CC1876F-F43F-4902-8C08-9F8194FFFO293',
            'lang': 'de',
            'activeExperimentId': 15,
            'email': username,
            'password': password,
            'limit': 16
        }

        r = requests.post(self.login_url, json=body, headers=self.non_auth_header)

        response = r.json()

        if 'err' in response:
            if response['err']['code'] == 'WRONG_CREDENTIALS':
                raise WrongCredentialsError
        elif 'code' in response:
            if response['code'] == 'CAPTCHA_REQUIRED':
                raise CaptchaRequiredError

        req_token = response['accessToken']
        self.req_token = req_token
        return req_token

    # coming-soonish
    #def __solve_captcha(self):
        #result = solver.hcaptcha(sitekey=self.captcha_key, url='tellonym.me', )

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

    def get_tells(self, limit):
        """
        Gets all Tells for the current user

        Returns:
            tells_array (array): all current tells for the user
        """
        payload = {'limit': limit}
        r = requests.get(self.get_tells_url, params=payload, headers=self.auth_header)
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
                'previousRouteName': 'Profile',
                'tell': text,
                'userId': id,
                'limit': 16,
                'contentType': "CUSTOM"
            }
        else:
            body = {
                'previousContentCount': 0,
                'previousRouteName': 'Profile',
                'tell': text,
                'userId': id,
                'limit': 16,
                'contentType': "CUSTOM"
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
            'limit': 16
        }

        # r = requests.post(self.delete_tell_url, json=body, headers=self.auth_header)
        
        r = requests.delete(self.delete_tell_url, params=id, headers = self.auth_header)

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
