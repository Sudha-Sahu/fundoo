from fundoo.main import app


def test_register():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/register/' page is posted to (POST)
    THEN check that a '405' or '200' status code is returned
    """
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        response = test_client.post('/register/')
        assert response.status_code == 405
        assert response.status_code == 200
