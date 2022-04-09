import pytest



@pytest.fixture(scope='function')
def user(db, django_user_model):
    user = django_user_model.objects.create_user(
        username='TestUser',
        email='test@test.com',
        password='TestPass123'
    )
    yield user

