import pytest
from authe.form import LoginForm
from django.contrib.auth import authenticate
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

@pytest.fixture
def valid_login_data():
    return  {
        "email": "valid@email.com",
        "password": "validPassword"
    }


@pytest.fixture
def invalid_login_data():
    return  {
        "email": "valid@gmail.com",
        "password": ""
    }


@pytest.fixture
def login_form(valid_login_data):
    form = LoginForm(valid_login_data)
    return form.is_valid()


@pytest.fixture
def auth(valid_login_data):
    user = authenticate(None, **valid_login_data)
    return user, user is not None


@pytest.fixture
def create_user(django_user_model, valid_login_data):
    user = django_user_model.objects.create_user(**valid_login_data)
    return user


@pytest.fixture
def response(auth):
    user, isNoNone = auth

    refresh = ""
    access = ""
    try:

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

    except: pass

    resp = Response({
        "access": access,
        "refresh": refresh
    })

    resp.set_cookie("access_token", access)
    resp.set_cookie("refresh_token", refresh)
    return resp


@pytest.mark.django_db
def test_login_form(create_user, login_form, auth):

    assert login_form
    user, isNoNone = auth
    assert isNoNone
    assert user == create_user


@pytest.mark.django_db
def test_login_response(create_user, response):

    assert isinstance(response, Response)
    assert isinstance(response.data, dict)
    assert response.data.get("refresh")
    assert response.data.get("access")
    assert response.cookies.get("access_token")
    assert response.cookies.get("refresh_token")

    try: 

        refresh = RefreshToken(response.data.get("refresh"))
        access = AccessToken(response.data.get("access"))

        access_token = AccessToken(response.cookies.get("access_token"))
        refresh_token = RefreshToken(response.cookies.get("refresh_token"))

        assert access == access_token
        assert refresh == refresh_token

    except TokenError as excinfo:
        assert False





