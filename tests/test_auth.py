from app.core.auth import create_access_token, verify_token

def test_verify_valid_token():
    token = create_access_token({"sub": "admin"})
    payload = verify_token(token)
    assert payload is not None
    assert payload["sub"] == "admin"

def test_verify_invalid_token():
    invalid_token = "this.is.invalid"
    payload = verify_token(invalid_token)
    assert payload is None
