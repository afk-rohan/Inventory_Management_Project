class UserManager:
    def __init__(self):
        self.users = {}

    def create_user(self, username, password, role):
        self.users[username] = {"password": password, "role": role}

    def authenticate(self, username, password):
        return username in self.users and self.users[username]["password"] == password

    def get_role(self, username):
        return self.users[username]["role"]
