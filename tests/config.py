from dataclasses import dataclass


@dataclass
class TestUser:
    email: str = "email@example.com"
    username: str = "username"
    password: str = "password"

    wrong_username: str = "wrong_username"
    wrong_password: str = "wrong_password"


test_user = TestUser()
