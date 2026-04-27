from password_validator import valider_mot_de_passe

def test_mot_de_passe_court():
    mdp = "user@"

    result = valider_mot_de_passe(mdp)

    assert result == False

def test_mot_de_passe_sans_majuscule():
    mdp = "user@1234"

    result = valider_mot_de_passe(mdp)

    assert result == False

def test_mot_de_passe_sans_chiffres():
    mdp = "uSer@test"

    result = valider_mot_de_passe(mdp)

    assert result == False

def test_mot_de_passe_sans_special():
    mdp = "uSertest21365"

    result = valider_mot_de_passe(mdp)

    assert result == False

def test_mot_de_passe_valide():
    mdp = "uSer@test21365"

    result = valider_mot_de_passe(mdp)

    assert result == True