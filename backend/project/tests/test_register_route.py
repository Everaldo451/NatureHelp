import pytest


@pytest.mark.django_db
def test_with_user_is_company(company_form, create_company_user,  create_company):

    user = create_company_user
    company = create_company

    assert company_form
    assert user is not None
    assert company is not None
