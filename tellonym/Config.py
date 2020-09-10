

class Config:

    def __init__(self, input):
        self.has_feed_ads = input['hasFeedAds']
        self.should_upload_contacts = input['shouldUploadContacts']
        self.reset_contacts_at = input['resetContactsAt']
        self.has_result_ads = input['hasResultAds']
        self.has_tells_ads = input['hasTellsAds']
        self.is_avatar_clickable = input['isAvatarClickable']
