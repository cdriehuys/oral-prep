import pytest
from quiz import models


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(email="test@example.com")


@pytest.mark.django_db
def test_question_str():
    q = models.Question.objects.create(
        certificate_type="PRIVATE",
        plane_type="ALL",
        question="What's the answer to life?",
        answer="42",
    )

    assert str(q) == f"Question {q.id}"


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


def test_preferences_get_questions_private(user):
    p = models.Preferences.objects.create(user=user, certificate_type="PRIVATE")

    q1 = models.Question.objects.create(
        certificate_type="PRIVATE", plane_type="ALL", question="q1", answer="a1"
    )
    models.Question.objects.create(
        certificate_type="COMMERCIAL", plane_type="ALL", question="q2", answer="a2"
    )

    assert list(p.get_applicable_questions()) == [q1]


def test_preferences_get_questions_commercial(user):
    p = models.Preferences.objects.create(user=user, certificate_type="COMMERCIAL")

    q1 = models.Question.objects.create(
        certificate_type="PRIVATE", plane_type="ALL", question="q1", answer="a1"
    )
    q2 = models.Question.objects.create(
        certificate_type="COMMERCIAL", plane_type="ALL", question="q2", answer="a2"
    )

    assert list(p.get_applicable_questions()) == [q1, q2]


def test_preferences_get_questions_no_planes(user):
    p = models.Preferences.objects.create(user=user, plane_type=None)

    always_applicable = models.Question.objects.create(
        certificate_type="PRIVATE",
        plane_type="ALL",
        question="What's the answer to life?",
        answer="42",
    )

    for plane in ["C152", "C172", "WARRIOR", "MOONEY"]:
        models.Question.objects.create(
            certificate_type="PRIVATE",
            plane_type=plane,
            question=f"{plane} question",
            answer=f"{plane} answer",
        )

    assert list(p.get_applicable_questions()) == [always_applicable]


def test_preferences_get_questions_all_planes(user):
    p = models.Preferences.objects.create(user=user, plane_type="ALL")

    models.Question.objects.create(
        certificate_type="PRIVATE",
        plane_type="ALL",
        question="What's the answer to life?",
        answer="42",
    )

    for plane in ["C152", "C172", "WARRIOR", "MOONEY"]:
        models.Question.objects.create(
            certificate_type="PRIVATE",
            plane_type=plane,
            question=f"{plane} question",
            answer=f"{plane} answer",
        )

    assert list(p.get_applicable_questions()) == list(models.Question.objects.all())


@pytest.mark.parametrize("plane", ["C152", "C172", "WARRIOR", "MOONEY"])
def test_preferences_get_questions_single_planes(user, plane):
    p = models.Preferences.objects.create(user=user, plane_type=plane)

    expected = [
        models.Question.objects.create(
            certificate_type="PRIVATE",
            plane_type="ALL",
            question="What's the answer to life?",
            answer="42",
        ),
        models.Question.objects.create(
            certificate_type="PRIVATE",
            plane_type=plane,
            question=f"{plane} question",
            answer=f"{plane} answer",
        ),
    ]

    for other_plane in ["C152", "C172", "WARRIOR", "MOONEY"]:
        if other_plane != plane:
            models.Question.objects.create(
                certificate_type="PRIVATE",
                plane_type=other_plane,
                question=f"{other_plane} question",
                answer=f"{other_plane} answer",
            )

    assert list(p.get_applicable_questions()) == expected
