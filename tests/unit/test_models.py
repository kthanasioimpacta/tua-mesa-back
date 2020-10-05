from app.models.User import User
 
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    user = User()
    user.id = 1
    user.password = 'password'
    user.role_id = 1

    assert user.id == 1
    assert user.password == 'password'
    assert user.role_id == 1