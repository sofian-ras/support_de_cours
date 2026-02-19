# Utilisation de l'image officiel nginx comme image de base
FROM nginx:latest

# Permet de préciser le répertoire de travail (équivalent à la commande cd)
WORKDIR /usr/share/nginx/html

# Run va permettre d'effectuer les commandes spécifié lors de la création de l'image
RUN rm -f ./* 
RUN apt update
RUN apt upgrade
RUN apt install -y nano

# Copie les fichier présent en local (la ou se trouve le dockerfile) vers le répertoire du conteneur (ici notre workdir)
COPY . .  

# Expose le port 80
EXPOSE 80

# Effectue la commande suivante à chaque lancement de conteneur (docker run)
CMD ["nginx", "-g", "daemon off;"]