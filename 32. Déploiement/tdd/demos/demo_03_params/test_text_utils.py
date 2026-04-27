import pytest
from text_utils import compter_lettres

@pytest.mark.parametrize("texte,resultat", [
    ("test test", 9),
    ("test", 4),
    ("", 0),
    ("test5", 5)
])
def test_compter_lettres(texte, resultat):
    assert compter_lettres(texte) == resultat

@pytest.fixture
def textes_exemples():
    return {
        "espace" : "test test",
        "vide" : "",
        "chiffre" : "test5"
    }

def test_compter_lettres_fixture(textes_exemples):
    assert compter_lettres(textes_exemples["espace"]) == 9
    assert compter_lettres(textes_exemples["vide"]) == 0
    assert compter_lettres(textes_exemples["chiffre"]) == 5