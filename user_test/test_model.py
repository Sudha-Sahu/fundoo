from fundoo.user.model import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, and password fields are defined correctly
    """
    user = User(user_name='Sudha Sahu', email='sudhasahu123@gmail.com', password='sudha123')
    assert user.user_name == 'Sudha Sahu'
    assert user.email == 'sudhasahu123@gmail.com'
    assert user.password != 'sudha123'
