from tellonym.Config import Config
from tellonym.Answer import Answer
from tellonym.Link import Link
from tellonym.Phone import Phone
from tellonym.Info import Info


class Profile:

    def __init__(self, client, input):
        self.__client = client
        self.id = input['id']
        self.email = input['email']
        self.display_name = input['displayName']
        self.username = input['username']
        self.type = input['type']
        self.language = input['lang']
        self.main_language = input['mainLanguage']
        self.location = input['location']
        self.page_id = input['pageId']
        self.twitter_username = input['twitterUsername']
        self.instagram_username = input['instagramUsername']
        self.is_email_notifications_enabled = input['isEmailNotificationsEnabled']
        self.email_polling_type = input['emailPollingType']
        self.creation_date = input['createdAt']
        self.is_safety_code_set = input['isSafetyCodeSet']
        self.twitter_id = input['twitterId']
        self.instagram_id = input['instagramId']
        self.theme = input['theme']
        self.about_me = input['aboutMe']
        self.avatar_file_name = input['avatarFileName']
        self.is_searchable = input['isSearchable']
        self.ad_free_until = input['adfreeUntil']
        self.last_active_at = input['lastActiveAt']
        self.likes_count = input['likesCount']
        self.follower_count = input['followerCount']
        self.anonymous_follower_count = input['anonymousFollowerCount']
        self.following_count = input['followingCount']
        self.tell_count = input['tellCount']
        self.answer_count = input['answerCount']
        self.occupation = input['occupation']
        self.phone = Phone(input['phone'])
        self.is_verified = input['isVerified']
        self.push_notification_token = input['pushNotificationToken']
        self.is_push_notifications_enabled = input['isPushNotificationsEnabled']
        self.is_push_notifications_enabled_system = input['isPushNotificationsEnabledSystem']
        self.is_push_notifications_tell_enabled = input['isPushNotificationsTellEnabled']
        self.is_push_notifications_answer_enabled = input['isPushNotificationsAnswerEnabled']
        self.is_push_notifications_liked_enabled = input['isPushNotificationsLikedEnabled']
        self.is_push_notifications_anonymous_subscription_enabled = \
            input['isPushNotificationsAnonymousSubscriptionEnabled']
        self.is_push_notifications_public_subscription_enabled = input['isPushNotificationsPublicSubscriptionEnabled']
        self.is_push_notifications_friend_created_post_enabled = input['isPushNotificationsFriendCreatedPostEnabled']
        self.is_push_notifications_user_tagged_enabled = input['isPushNotificationsUserTaggedEnabled']
        self.is_push_notifications_messages_enabled = input['isPushNotificationsMessageEnabled']
        self.phone_prefix = input['phonePrefix'] # Region code without + (e.g 49)
        self.phone_suffix = input['phoneNumber'] # Default number -> 123456
        self.phone_number = self.phone_prefix + self.phone_suffix
        self.is_tells_only_from_registered = input['isTellsOnlyFromRegistered']
        self.is_allowed_to_moderate = input['isAllowedToModerate']
        self.link_data = self.__get_link_data(input['linkData'])
        self.has_allowed_emails = input['hasAllowedEmails']
        self.hasAllowedSearchByPhone = input['hasAllowedSearchByPhone']
        self.hasAllowedShowActivity = input['hasAllowedShowActivity']
        self.is_under_16 = input['isUnder16']
        self.parental_email = input['parentalEmail']
        self.safety_level_sex_harass = input['safetyLevelSexHarass']
        self.safety_level_insult = input['safetyLevelInsult']
        self.safety_level_spam = input['safetyLevelSpam']
        self.has_password = input['hasPassword']
        self.is_twitter_connected = input['isTwitterConnected']
        self.is_precise_birthdate = input['isPreciseBirthdate']
        self.gender = input['gender']
        self.birthdate = input['birthdate']
        self.has_allowed_featuring = input['hasAllowedFeaturing']
        self.has_allowed_show_age = input['hasAllowedShowAge']
        self.has_allowed_search_by_location = input['hasAllowedSearchByLocation']
        # self.city = input['city']
        # self.country = input['country']
        self.answers = self.__get_answers(input['answers'])
        self.config = Config(input['config'])

        ## New
        self.status_emoji = input['statusEmoji']
        self.occupation = input['occupation']
        self.pinned_posts = input['pinnedPosts']
        self.is_verification_recommended = input['isVerificationRecommended']
        self.premium_until = input['premiumUntil']
        self.is_apple_connected = input['isAppleConnected']
        self.is_premium = input['isPremium']
        self.info = Info(input['info'])
        self.ad_exp_id = input['adExpId']
        self.is_secure_account_recommended = input['isSecureAccountRecommended']
        self.available_badges = input['availableBadges']
        self.tgt  = input['tgt'] # what is this? Update: 09/10/21 Still no idea
        self.tint_color = input['tintColor']
        self.badge = input['badge']
        self.is_google_connected = input['isGoogleConnected']


    def __get_link_data(self, input):
        """
        Gets the linked accounts from the current user

        Args:
            input (json str): link data input

        Returns:
            Link (class): linked data information
        """

        link_data = []
        for index, _ in enumerate(input):
            link = Link(input[index])
            link_data.append(link)

        return link_data

    def __get_answers(self, input):
        """
        Gets all answers on the current user's profile

        Args:
            input (json str): array of answers

        Returns:
            answers (arr): array of answer classes
        """
        answers = []
        for index, _ in enumerate(input):
            answer = Answer(self.__client, input[index])
            answers.append(answer)

        return answers

    def is_default_phonenumber(self):
        """
        Checks wether or not the phonenumber is default

        Returns:
            True: If phonenumber is default
            False: If phonenumber is not default
        """

        if self.phone_suffix == 12345678:
            return True
        return False
