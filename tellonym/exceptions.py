WrongCredentialsError = Exception('you have provided a wrong username password combination')
UnauthorizedError = Exception('we failed to provide a correct auth_token. are you logged in?')
TellNotFoundError = Exception('tell with the tell_id you provided does not exist')
UserNotFoundError = Exception('the user_id you have entered does not belong to any user.')
InvalidParameterError = \
    Exception('an invalid parameter was send to the api endpoint. please contact the author of this module')
UnknownError = Exception('an unknown error has occured, please inform the author of this module')
CaptchaRequiredError = Exception('we have encountered a captcha. please try again later')
