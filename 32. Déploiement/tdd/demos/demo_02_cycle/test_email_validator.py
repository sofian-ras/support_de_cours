import pytest
from email_validator import valider_email

def test_email_valide():
    email = "user@email.com"

    result = valider_email(email)

    assert result == True

def test_email_sans_arobase():
    email = "useremail.com"

    result = valider_email(email)

    assert result == False

# Tests après refractor

def test_email_sans_domaine():
    email = "user@"

    result = valider_email(email)

    assert result == False

def test_email_sans_extension():
    email = "user@email"

    result = valider_email(email)

    assert result == False

def test_email_avec_points():
    email = "user.name@email.com"

    result = valider_email(email)

    assert result == True