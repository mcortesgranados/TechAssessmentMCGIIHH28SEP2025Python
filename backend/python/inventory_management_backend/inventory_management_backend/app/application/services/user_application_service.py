class UserApplicationService:
    def authenticate_user(self, username: str, password: str):
        if username == "admin" and password == "secret123":
            class User: pass
            user = User()
            user.username = "admin"
            return user
        return None