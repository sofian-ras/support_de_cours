import os

nom = os.getenv("NOM", "invité")
age = os.getenv("AGE", "0")

print(f"Bonjour, {nom}! vous avez {age} ans")