import pytest
from temperature import convertir_temperature

@pytest.mark.parametrize("valeur,source,cible,attendu", [
    # Conversions depuis Celsius
    (0, "C", "F", 32.0),
    (100, "C", "F", 212.0),
    (0, "C", "K", 273.15),
    (100, "C", "K", 373.15),
    (-40, "C", "F", -40.0),
    
    # Conversions depuis Fahrenheit
    (32, "F", "C", 0.0),
    (212, "F", "C", 100.0),
    (32, "F", "K", 273.15),
    (212, "F", "K", 373.15),
    
    # Conversions depuis Kelvin
    (273.15, "K", "C", 0.0),
    (373.15, "K", "C", 100.0),
    (273.15, "K", "F", 32.0),
    (373.15, "K", "F", 212.0),
    
    # Même unité
    (25, "C", "C", 25.0),
    (77, "F", "F", 77.0),
    (300, "K", "K", 300.0)
])
def test_convertir_temperature(valeur, source, cible, attendu):
    assert convertir_temperature(valeur, source, cible) == attendu

@pytest.mark.parametrize("valeur,source,cible", [
    (100, "C", "A"),
    (100, "C", "f"),
    (100, "A", "C")
])
def test_unites_invalides(valeur, source, cible):
    with pytest.raises(ValueError):
        convertir_temperature(valeur, source, cible)
