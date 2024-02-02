#o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
#Logiciel de mémorisation
#Auteur : Clément Denève
#o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o

#o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o Importations o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
import tkinter as tk
from tkinter.font import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import PIL.Image
import PIL.ImageTk
import pickle
import random

#o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o Classe Application o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
class Memoreasy():
    #x-x-x-x-x-x-x-x Initialisation x-x-x-x-x-x-x-x-x-x-x-x-x
    def __init__(self, master):
        #Attributs
        self.master = master                                        #Fenêtre principale de tkinter
        self.fontBoutons = Font(size = 30)                          #Taille de la police dans les boutons de l'application
        self.rangTableau = 0                                        #Indice qui repère le numéro d'une carte dans un dossier donné
        self.choixChapitre = 0                                      #Numéro du chapitre choisi
        self.tableauDonneesTexte = []                               #Tableau du dossier choisi [numéro, fonction, description, lien, nombredefoiscarteretournée, compteur_positif_negatif]
        self.tableauStats = []
        self.pageActive = "commencer"
        self.modeApprentissage = 'lineaire'

        #Recupération de la taille de l'écran
        self.hauteurEcran = self.master.winfo_screenheight()        #Hauteur de l'écran 
        self.largeurEcran = self.master.winfo_screenwidth()         #Largeur de l'écran
        self.centreFenetre = (self.hauteurEcran//2,self.largeurEcran//2)
        self.maxwidth = int(self.largeurEcran * (80/100))
        print("Taille de l'écran : ",str(self.hauteurEcran)+' x '+str(self.largeurEcran))
        print("Position centre : ",self.centreFenetre)

        #Appel de l'affichage
        self.affichage_global_Menu()
        self.affichage_global_Fenetre()

        #Interactions utilisateurs
        self.master.bind('<KeyPress-Right>',self.raccourci_clavier_flecheDroite)
        self.master.bind_all('<KeyPress-Left>',self.raccourci_clavier_flecheGauche)
        self.master.bind_all('<KeyPress-space>',self.raccourci_clavier_barreEspace)


    #x-x-x-x-x-x-x-x Affichage x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
    #Affichage global
    def affichage_global_Fenetre(self):
        #Configuration du root
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.affichage_page_commencer()
    def affichage_global_Menu(self):
        menuBar = tk.Menu(self.master, relief = 'flat', bg = "#f7f7f7", fg = "#727272", activebackground = "#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        police = Font(size = 10)
        
        #Création des onglets
        fichier = tk.Menu(menuBar, tearoff=0, relief=tk.FLAT, bg="#f7f7f7", fg="#727272", activebackground="#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        statist = tk.Menu(menuBar, tearoff=0, relief=tk.FLAT, bg="#f7f7f7", fg="#727272", activebackground="#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        paramet = tk.Menu(menuBar, tearoff=0, relief=tk.FLAT, bg="#f7f7f7", fg="#727272", activebackground="#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        chapitres = tk.Menu(menuBar, tearoff=0, relief=tk.FLAT, bg="#f7f7f7", fg="#727272", activebackground="#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        aidmenu = tk.Menu(menuBar, tearoff=0, relief=tk.FLAT, bg="#f7f7f7", fg="#727272", activebackground="#2a8eff", activeborderwidth = 0, border = 0, activeforeground = "#f7f7f7")
        
        #Création des sous menus

        #Fichier
        fichier.add_command(label="Sauvegarder deck en cours", command = self.fonction_sauvegardeDeck, font = police)
        fichier.add_command(label="Ouvrir un fichier texte", command = self.fonction_ouvrirTexteAncien, font = police)
        fichier.add_command(label="Quitter", command = self.master.destroy, font = police)
        #Edition
        statist.add_command(label="Voir les statistiques", font=police)
        statist.add_command(label="Réinitialiser les statistiques pour le chapitre en cours", font=police, command=self.stat_reinitialiser)

        #Paramètres
        paramet.add_command(label="Mode d'apprentissage linéaire",  font=police, command=self.fonction_bouton_mode_lineaire)
        paramet.add_command(label="Mode d'apprentissage aléatoire",  font=police, command=self.fonction_bouton_mode_aleatoire)

        #Liste des chapitres
        chapitres.add_command(label='Chapitre 4 : Intégration',  font = police, command=self.chapitre_maths4)
        chapitres.add_command(label='Chapitre 16 : Equations différentielles',  font = police, command=self.chapitre_maths16)
        chapitres.add_command(label='Chapitre 17 : Fonctions vectorielles - Arc paramétrés',  font = police, command=self.chapitre_maths17)
        #Aide
        aidmenu.add_command(label="Aide",  font=police, command=self.fonction_aide)
        
        
        #Création des menus défilants
        menuBar.add_cascade(label="Fichier", menu=fichier, font=police)
        menuBar.add_cascade(label="Statistiques", menu=statist, font=police)
        menuBar.add_cascade(label="Paramètres", menu=paramet, font=police)
        menuBar.add_cascade(label="Chapitres", menu=chapitres, font=police)
        menuBar.add_cascade(label="Aide", menu=aidmenu, font=police)
        
        #Ajout du menu
        self.master.config(menu = menuBar)
    #Affichage des différentes pages
    def affichage_page_commencer(self):
        self.pageActive = 'commencer'
        #Configuration du cadre global
        self.framePrincipal = tk.Frame(self.master, bg='#F3FDFF')
        self.framePrincipal.columnconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(1, weight=2)


        #Configuration du frame des boutons
        self.frameBoutons = tk.Frame(self.framePrincipal, bg='darkgrey')
        self.frameBoutons.rowconfigure(0, weight=1)
        self.frameBoutons.columnconfigure(0, weight=1)

        #Configuration du bouton retourner
        self.boutonCommencer = tk.Button(self.frameBoutons, text='Bienvenue sur Memoreasy - Mathématiques', font=self.fontBoutons, bg='mediumaquamarine', command=self.fonction_bouton_commencer)
        self.boutonCommencer.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')


        #grid des éléments
        self.framePrincipal.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')
        

        #Affichage du logo
        imagelogo = PIL.Image.open('data/images/digital_brain1.PNG')

        #Adaptation des images pour qu'elle soit dans la fenêtre
        self.ratio = 700/ float(imagelogo.size[0])
        self.hsize=int((float(imagelogo.size[1])*float(self.ratio)))
        self.image = imagelogo.resize((700,self.hsize),PIL.Image.LANCZOS)

        #Creation de la matrice PIL
        self.photo = PIL.ImageTk.PhotoImage(imagelogo)
        self.photo.image = self.image
        self.imageWidth, self.imageHeight = imagelogo.size
        self.canvasPrincipal = tk.Canvas(self.framePrincipal,height=self.imageHeight ,width=self.imageWidth, bg='white', border=0) 
        self.canvasPrincipal.create_image(self.imageWidth/2,self.imageHeight/2,image=self.photo)
        self.canvasPrincipal.grid(row=0, column=0)
        self.frameBoutons.grid(row=1, column=0, padx=5, pady=5)
    def affichage_page_carteFace(self):
        self.pageActive = 'carteFace'
        #Enlever tous les widgets de la page précédente
        for widget in self.master.winfo_children(): widget.grid_forget();

        #Configuration du cadre global
        self.framePrincipal = tk.Frame(self.master, bg='#F3FDFF')
        self.framePrincipal.columnconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(1, weight=2)
        self.framePrincipal.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')

        self.frameBoutons = tk.Frame(self.framePrincipal, bg='darkgrey')
        self.frameBoutons.rowconfigure(0, weight=1)
        self.frameBoutons.columnconfigure(0, weight=1)
        self.frameBoutons.grid(row=1, column=0, padx=5, pady=5)
        self.boutonRetourner = tk.Button(self.frameBoutons, text='Retourner la carte', bg='mediumaquamarine', font=self.fontBoutons,  command=self.fonction_bouton_retournerLaCarte)
        self.boutonRetourner.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        #Affichage du label
        self.labelPrincipal = tk.Label(self.framePrincipal, font=self.fontBoutons, text=self.tableauDonneesTexte[self.rangTableau][2], wraplength=1000, bg='#F3FDFF')
        self.labelPrincipal.grid(row=0, column=0)
    def affichage_page_cartePile(self):
        self.pageActive = 'cartePile'
        #Enlever tous les widgets de la page précédente
        for widget in self.master.winfo_children(): widget.grid_forget();

        #Configuration du cadre global
        self.framePrincipal = tk.Frame(self.master, bg='#F3FDFF')
        self.framePrincipal.columnconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(0, weight=10)
        self.framePrincipal.rowconfigure(1, weight=2)
        self.framePrincipal.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')

        #Affichage des boutons raté / réussi dans un frame Boutons
        self.frameBoutons = tk.Frame(self.framePrincipal, bg='darkgrey')
        self.frameBoutons.rowconfigure(0, weight=1)
        self.frameBoutons.columnconfigure(0, weight=1)
        self.frameBoutons.columnconfigure(1, weight=1)
        self.frameBoutons.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.boutonNul = tk.Button(self.frameBoutons, text='Raté', bg='crimson', font=self.fontBoutons, command=self.fonction_bouton_rate)
        self.boutonParfait = tk.Button(self.frameBoutons, text='Réussi', bg='lightgreen', font=self.fontBoutons, command=self.fonction_bouton_reussi)
        self.boutonNul.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.boutonParfait.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.image = self.tableauDonneesTexte[self.rangTableau][6]

        #Adaptation de l'image pour qu'elle soit dans la fenêtre
        self.ratio = self.maxwidth/ float(self.image.size[0])
        self.hsize=int((float(self.image.size[1])*float(self.ratio)))
        self.image = self.image.resize((self.maxwidth,self.hsize),PIL.Image.ANTIALIAS)

        #Creation de la matrice PIL
        self.photo = PIL.ImageTk.PhotoImage(self.image)
        self.photo.image = self.image
        self.imageWidth, self.imageHeight = self.image.size

        #Création de la nouvelle image
        self.canvasPrincipal = tk.Canvas(self.framePrincipal,height=self.imageHeight ,width=self.imageWidth, bg='white') 
        self.canvasPrincipal.create_image(self.imageWidth/2,self.imageHeight/2,image=self.photo)
        self.canvasPrincipal.grid(row=0, column=0)
    def affichage_page_finDuDeck(self):
        self.pageActive = 'finDuDeck'
        #Enlever tous les widgets de la page précédente
        for widget in self.master.winfo_children(): widget.grid_forget();

        #Configuration du cadre global
        self.framePrincipal = tk.Frame(self.master, bg='#F3FDFF')
        self.framePrincipal.columnconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.rowconfigure(1, weight=1)
        self.framePrincipal.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')

        #Affichage label 'fin du deck'
        self.labelPrincipal = tk.Label(self.framePrincipal, font=self.fontBoutons, text='Fin du deck - Veuillez choisir un nouveau chapitre', wraplength=1000, bg='#F3FDFF')
        self.labelPrincipal.grid(row=0, column=0)
        self.labelPrincipal = tk.Label(self.framePrincipal, font=self.fontBoutons, text='Espace pour relancer', wraplength=1000, bg='#F3FDFF')
        self.labelPrincipal.grid(row=1, column=0)
    def affichage_page_aide(self):
        self.pageActive = 'aide'
        #Enlever tous les widgets de la page précédente
        for widget in self.master.winfo_children(): widget.grid_forget();

        #Configuration du cadre global
        self.framePrincipal = tk.Frame(self.master, bg='#F3FDFF', heigh=500, width=900)
        self.framePrincipal.columnconfigure(0, weight=10)
        self.framePrincipal.columnconfigure(1, weight=10)
        self.framePrincipal.columnconfigure(2, weight=1)
        self.framePrincipal.rowconfigure(0, weight=1)
        self.framePrincipal.grid(row=0, column=0, padx=1, pady=1, sticky='nsew')

        #Appel du fichier texte
        fichier_aide = open('data/help.txt', 'r')
        lignes = fichier_aide.readlines()
        texte = ''
        for i in lignes:
            texte = texte+'\n'+i
        fichier_aide.close()


        #Creation de la scrollbar
        scrollbar = tk.Scrollbar(self.framePrincipal, width=30)
        textWidget = tk.Text(self.framePrincipal)
        framechoix = tk.Frame(self.framePrincipal, )
        scrollbar.config(command=textWidget.yview)
        textWidget.config(yscrollcommand=scrollbar.set)
        textWidget.insert(tk.END, texte)

        #Affichage dans la grille
        scrollbar.grid(row=0, column=2, sticky='ns' )
        textWidget.grid(row=0, column=1, sticky='nsew')
        framechoix.grid(row=0, column=0, sticky='nsew')


    #x-x-x-x-x-x-x-x Fonctions utilitaires x-x-x-x-x-x-x-x-x-x
    def fonction_ouvrirTexte(self):
        #Réinitialisation de l'indice de la carte actuelle
        self.rangTableau = 0

        #Extraction des données
        donnees = open('data/chapitres/'+self.nomDeck,'rb')
        self.tableauDonneesTexte = pickle.load(donnees)
        donnees.close()

        if self.modeApprentissage == 'aleatoire':
            random.shuffle(self.tableauDonneesTexte)
    def fonction_ouvrirTexteAncien(self):
        #Enregistrement des données dans un tableau
        chemin = askopenfilename(title="Ouvrir une fichier texte", filetypes=[('all files','.*')])

        #Récolte des données
        fichier = open(chemin, "r")
        textebrut = fichier.readlines()
        fichier.close()

        #Traitement des données
        self.tableauDonneesTexte = []
        for i in textebrut:
            i = i.rstrip('\n')
            i = i.split(', ')
            i.append('data/cartes/'+i[0]+'.PNG')
            self.tableauDonneesTexte.append(i)

        #Enregistrement du nom du fichier
        print(chemin)
        chemin = chemin.split('/')
        print(chemin)
        chemin = chemin[len(chemin)-1]
        print(chemin)
        chemin = chemin.split('.')
        self.nomDeck = chemin[0]
    def fonction_sauvegardeDeck(self):
        #Ouverture du fichier en mode écriture binaire
        fichier = open('data/chapitres/'+self.nomDeck,'wb')

        #Ecriture du dictionnaire
        pickle.dump(self.tableauDonneesTexte,fichier)

        #Fermeture du fichier
        fichier.close()
    def fonction_aide(self):

        self.affichage_page_aide()

    #x-x-x-x-x-x-x-x Fonctions Boutons x-x-x-x-x-x-x-x-x-x-x-x
    def fonction_bouton_reussi(self):
        self.tableauDonneesTexte[self.rangTableau][3] = int(self.tableauDonneesTexte[self.rangTableau][3]) + 1
        self.tableauDonneesTexte[self.rangTableau][4] = int(self.tableauDonneesTexte[self.rangTableau][4]) + 1

        self.rangTableau += 1
        if self.rangTableau < len(self.tableauDonneesTexte):
            self.affichage_page_carteFace()
        else:
            self.affichage_page_finDuDeck()
            self.choixChapitre = 0
            self.fonction_sauvegardeDeck()
    def fonction_bouton_rate(self):
        self.tableauDonneesTexte[self.rangTableau][3] = int(self.tableauDonneesTexte[self.rangTableau][3]) + 1
        self.tableauDonneesTexte[self.rangTableau][4] = int(self.tableauDonneesTexte[self.rangTableau][4]) - 1

        self.rangTableau += 1
        if self.rangTableau < len(self.tableauDonneesTexte):
            self.affichage_page_carteFace()
        else:
            self.affichage_page_finDuDeck()
            self.choixChapitre = 0
            self.fonction_sauvegardeDeck()
    def fonction_bouton_retournerLaCarte(self):
        #Fonction d'appui sur le bouton "Retourner la carte"
        self.affichage_page_cartePile()
    def fonction_bouton_commencer(self):
        #Choisir le chapitre
        if self.choixChapitre == 0:
            return 0

        self.affichage_page_carteFace()
    def fonction_bouton_mode_lineaire(self):
        #On passe en mode apprentissage linéaire
        self.modeApprentissage = 'lineaire'
    def fonction_bouton_mode_aleatoire(self):
        #On passe en mode d'apprentissage aléatoire
        self.modeApprentissage = 'aleatoire'



    #x-x-x-x-x-x-x-x Fonctions de statistiques x-x-x-x-x-x-x-x
    def stat_sauvegarde(self):
        fichier=open(self.choixChapitre,"w")
        texte=fichier.readlines()
        fichier.close()
    def stat_reinitialiser(self):
        print(self.tableauDonneesTexte)
        for ligne in self.tableauDonneesTexte:
            ligne[3] = '0'
            ligne[4] = '0'
        print(self.tableauDonneesTexte)


    #x-x-x-x-x-x-x-x Autre x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
    #Chapitres
    def chapitre_maths16(self):
        self.choixChapitre = "dossiers/Mathématiques/maths16_equations_differentielles.txt"
        self.nomDeck = 'Mathématiques_Chapitre_16'
        self.fonction_ouvrirTexte()
        print(self.tableauDonneesTexte)
    def chapitre_maths17(self):
        self.nomDeck = 'Mathématiques_Chapitre_17'
        self.choixChapitre = "dossiers/Mathématiques/maths17_fonctions_vectorielles_arcs_parametres.txt"
        self.fonction_ouvrirTexte()
    def chapitre_maths4(self):
        self.nomDeck = 'Mathématiques_Chapitre_4'
        self.choixChapitre = "dossiers/Mathématiques/maths4_integration.txt"
        self.fonction_ouvrirTexte()

    #Raccourcis claviers
    def raccourci_clavier_barreEspace(self,a):
        if self.pageActive == 'commencer':
            self.fonction_bouton_commencer()
        if self.pageActive == 'carteFace':
            self.fonction_bouton_retournerLaCarte()
        if self.pageActive == 'finDuDeck' and self.choixChapitre != 0:
            self.fonction_bouton_commencer()
    def raccourci_clavier_flecheDroite(self,a):
        if self.pageActive == 'cartePile':
            self.fonction_bouton_reussi()
    def raccourci_clavier_flecheGauche(self,a):
        if self.pageActive == 'cartePile':
            self.fonction_bouton_rate()






#o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o Programme Principal o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o
def main():
    root = tk.Tk()
    root.title("Memoreasy - Mathématiques")
    root.wm_state('zoomed')
    Memoreasy(root)
    root.mainloop()
if __name__ == "__main__":
    main()