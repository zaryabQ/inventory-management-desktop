# user.py

class User:
    current_user = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    @classmethod
    def set_current_user(cls, username, password):
        cls.current_user = cls(username, password)

    @classmethod
    def get_current_user(cls):
        return cls.current_user

    @classmethod
    def clear_current_user(cls):
        cls.current_user = None
