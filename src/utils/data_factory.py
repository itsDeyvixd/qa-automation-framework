"""
Test data factory using Faker.
Credentials for DummyJSON: https://dummyjson.com/docs/auth
"""
from faker import Faker

fake = Faker()


class UserFactory:
    @staticmethod
    def valid_payload() -> dict:
        return {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
            "age": fake.random_int(min=18, max=60),
        }

    @staticmethod
    def updated_payload() -> dict:
        return {
            "firstName": fake.first_name(),
            "lastName": fake.last_name(),
        }

    @staticmethod
    def patch_payload() -> dict:
        return {"age": fake.random_int(min=18, max=60)}


class AuthFactory:
    VALID_LOGIN = {
        "username": "emilys",
        "password": "emilyspass",
    }

    @staticmethod
    def missing_password() -> dict:
        return {"username": "emilys"}

    @staticmethod
    def missing_username() -> dict:
        return {"password": "emilyspass"}

    @staticmethod
    def invalid_credentials() -> dict:
        return {
            "username": fake.user_name(),
            "password": fake.password(),
        }
