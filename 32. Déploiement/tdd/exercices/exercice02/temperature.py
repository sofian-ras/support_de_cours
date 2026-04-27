def convertir_temperature(valeur, source, cible):
    unites = ["C", "F", "K"]

    if cible not in unites or source not in unites:
        raise ValueError()
    
    if source == cible:
        return round(valeur, 2)
    
    if source == "C":
        celsius = valeur
    elif source == "F":
        # C = (F - 32) × 5/9
        celsius = (valeur - 32) * 5/9
    else:
        # C = K - 273.15
        celsius = valeur - 273.15

    if cible == "C":
        resultat = celsius
    elif cible == "F":
        # F = (C × 9/5) + 32
        resultat = (celsius * 9/5) + 32
    else:
        # K = C + 273.15
        resultat = celsius + 273.15

    return round(resultat, 2)