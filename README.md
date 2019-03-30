# Memoreasy - Description 
Memoreasy est un logiciel de mémorisation de cartes mémoires (flashcards) écrit en python 3.X, utilisant la Programmation Orentientée Objet (POO). Ce projet m'a permis de me familiariser avec la programmation évènementielle en python, grâce à une interface interactive.
 
Modules utilisés : 
 - tkinter pour l'interface graphique
 - Pillow alias PIL pour le traitement d'image
 - pickle pour enregistrer les données d'un chapitre dans un fichier en hexadecimal
 - random pour générer des séquences de révision aléatoires

Fonctions du script :
 - Réviser un chapitre de cours théorème par théorème, en répondant pour chaque énoncé par "raté" ou "réussi" pour avoir des statistiques concernant chaque énoncé (Nombre de fois où l'énoncé à été vu, nombre de fois réussi, nombre de fois raté...)
 - Enregistrer, un chapitre de cours sous format hexadécimal
 - Changer de chapitre à tout moment
 - Mettre en mode "apprentissage aléatoire" pour que l'application affiche des énoncés aléatoire du chapitre en cours.
 
# Memoreasy - Installation

Pour l'installation il faut télécharger le .zip via github, il comprend le script et le dossier contenant les images utiles à l'affichage de l'interface graphique ainsi que les chapitres de test.
Il faut également une version python 3.x avec les bons modules. Ils sont en général compris dans le téléchargement de python sauf pickle.

Pour installer les modules utilisés via cmd sous windows (Penser à mettre python dans le windows PATH) 

 #python -m pip install random
 
 #python -m pip install tkinter
 
 #python -m pip install Pillow
 
 #python -m pip install pickle

# Memoreasy - Améliorations

Fonctions et idées à implémenter quand j'aurais le temps
 - Consultation des statistiques par une page spéciale
 - Pouvoir ajouter ses propres cartes/decks directement depuis l'application
 - Les cartes sont affichées en fonction des statistiques (plus on rate une carte plus celle-ci s'affiche souvent pour mieux la retenir)
 - Rendre l'interface plus propre
