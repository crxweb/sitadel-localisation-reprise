# sitadel-localisation-reprise

Exemple d'utilisation de la librairie Python Pandas dans le cadre d'une reprise de données MYSQL.

L'enjeu était de reconstruire des table de localisation (villes, codes postaux..) dont les données étaient devenues obsolètes, incohérentes et dont certaines étaient mal encodées suite à la possibilité pour les utilisateurs d'alimenter certaines tables.

Pandas a été utile pour détecter ces incohérences et générer les nouvelles tables en utilisant conjointement des set de données fiables et l'utilisation de web services.


[Point d'entrée à editer au besoin - refonte_localisation.py](refonte_localisation.py)
