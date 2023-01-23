from models import UserLogin
from datetime import datetime as dt
import pytest


@pytest.fixture
def fake_user():
    fake_user = {
        "user_id": "user",
        "device_type": "mac",
        "masked_ip": "111",
        "masked_device_id": "222",
        "app_version": 1,
        "create_date": dt.today().date(),
    }
    return fake_user


class TestConfig:
    def test_settings(self):
        from config import settings

        assert settings.POSTGRES_USER == "postgres"


class TestDatabase:
    def test_db(self):
        # from database import write_login
        assert True
        # add tests ...


class TestModels:
    def test_UserLogin(self, fake_user):
        # use a fixture in practic
        login = UserLogin(**fake_user)
        assert login.user_id == "user"

    def test_missingFields(self, fake_user):
        del fake_user["masked_ip"]
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            UserLogin(**fake_user)
