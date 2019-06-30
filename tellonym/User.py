import json

class User:

    def __init__(self, input):
        self.id = input['id']
        self.display_name = input['displayName']
        self.username = input['username']
        self.page_id = input['pageId']
        self.about_me = input['aboutMe']
        self.avatar_file_name = input['avatarFileName']
        self.is_verified = input['isVerified']
        self.is_active = input['isActive']

    def get_profile_picture(self):
        return 'userimg.tellonym.me/xs/' + self.avatar_file_name

    def get_profile_thumbnail(self):
        return 'userimg.tellonym.me/thumb/' + self.avatar_file_name
