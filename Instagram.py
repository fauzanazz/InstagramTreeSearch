import instaloader


class Instagram:
    """Instagram class to interact with Instagram API using Instaloader library"""

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.L = instaloader.Instaloader()

    def login(self) -> tuple[bool, str]:
        """
        Login to Instagram account using provided credentials
        :return: tuple of login status and message
        """
        try:
            self.L.login(self.username, self.password)
            print("Login successful")
            return True, "Login successful"

        except instaloader.exceptions.BadCredentialsException:
            print("Login failed")
            return False, f"Login failed for {self.username}, bad credentials"

        except instaloader.exceptions.ConnectionException:
            print("Login failed")
            return False, f"Login failed for {self.username}, connection error"

        except Exception as e:
            print("Login failed")
            return False, f"Login failed for {self.username}, {e}"

    def get_profile(self, target_username) -> instaloader.Profile | None:
        """
        Get profile metadata of a target username
        :param target_username: str, username of the target profile
        :return: instaloader.Profile object or None
        """
        try:
            profile = instaloader.Profile.from_username(self.L.context, target_username)
            return profile

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"Profile {target_username} does not exist")
            return None

        except instaloader.exceptions.ConnectionException:
            print("Connection error")
            return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_followers(self, target_username) -> list[instaloader.Profile] | None:
        """
        Get followers of a target profile
        :param target_username: str, username of the target profile
        :return: list of instaloader.Profile objects or None
        """
        try:
            profile = self.get_profile(target_username)
            if profile:
                followers = [follower for follower in profile.get_followers()]
                return followers

            return None

        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_following(self, target_username) -> list[instaloader.Profile] | None:
        """
        Get following of a target profile
        :param target_username: str, username of the target profile
        :return: list of instaloader.Profile objects or None
        """
        try:
            profile = self.get_profile(target_username)
            if profile:
                following = [following for following in profile.get_followees()]
                return following

            return None

        except Exception as e:
            print(f"Error: {e}")
            return None