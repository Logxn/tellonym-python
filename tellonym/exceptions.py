WrongCredentialsError = Exception('you have provided a wrong username password combination')
UnauthorizedError = Exception('we failed to provide a correct auth_token. are you logged in?')
UserNotFoundError = Exception('the user_id you have entered does not belong to any user.')
