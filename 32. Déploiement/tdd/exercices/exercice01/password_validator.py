import re

def valider_mot_de_passe(mdp):
    if len(mdp) < 8:
        return False
    if re.search(r"[A-Z]", mdp) is None:
        return False
    if re.search(r"[0-9]", mdp) is None:
        return False
    if re.search(r"[@#$%&]", mdp) is None:
        return False
    return True