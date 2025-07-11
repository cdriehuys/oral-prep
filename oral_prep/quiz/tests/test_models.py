import pytest
from quiz import models


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(email="test@example.com")


def test_preferences_for_user_default(user):
    preferences = models.Preferences.for_user(user)

    assert preferences.certificate_type == "PRIVATE"
    assert preferences.plane_type is None


def test_preferences_for_user_existing(user):
    preferences = models.Preferences.objects.create(
        user=user, certificate_type="COMMERCIAL", plane_type="C172"
    )
    saved = models.Preferences.for_user(user)

    assert saved == preferences
