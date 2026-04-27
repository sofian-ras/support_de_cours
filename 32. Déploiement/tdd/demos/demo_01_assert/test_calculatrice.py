import pytest
from calculatrice import additionner, diviser

def test_additionner_nombres_positifs():
    a, b = 3, 5

    result = additionner(a, b)

    assert isinstance(a, int)
    assert isinstance(b, int)
    assert isinstance(result, int)
    assert result == 8
    
def test_additionner_nombres_negatifs():
    a,b = -2, -3

    result = additionner(a,b)

    assert result == -5

def test_diviser_nombres_valides():
    a,b = 10, 2

    result = diviser(a, b)

    assert result == 5

def test_diviser_par_zero():
    a, b = 10, 0

    with pytest.raises(ValueError, match="Division par zéro impossible"):
        diviser(a,b)