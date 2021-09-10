class Phone:
    def __init__(self, input):
        self.prefix = input['prefix'] # Region Code (e.g. +49)
        self.number = input['number'] # Censored Number (e.g. **********37)
