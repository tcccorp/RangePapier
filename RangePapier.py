# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import *
import glob
import hashlib
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import time
import os
import re
from lxml import etree
from wand.image import Color
from wand.image import Image as ImageWand


	
class Ui_MainWindow(object):


	
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1260, 1000)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")	
        self.label = QLabel(MainWindow)
        pixmap = QPixmap('W:\scan_documents\image2017-07-08-195950-4.jpg')
        self.label.setPixmap(pixmap)
        self.label.setGeometry(QtCore.QRect(450, 30, 800, 950))
        self.label.setScaledContents(1)
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(5, 50, 441, 900))
        self.listWidget.setObjectName("listWidget")		
        self.listWidget.doubleClicked.connect(self.clickMethod)
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(5, 10, 341, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(350, 10, 93, 28))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect (lambda:self.rechercheMot(self.textEdit.toPlainText()))		
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1276, 26))
        self.menubar.setObjectName("menubar")
        self.menuFichiers = QtWidgets.QMenu(self.menubar)
        self.menuFichiers.setObjectName("menuFichiers")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAffiche_Fichiers = QtWidgets.QAction(MainWindow)
        self.actionAffiche_Fichiers.setObjectName("actionAffiche_Fichiers")		
        self.actionOCR_sur_fichiers = QtWidgets.QAction(MainWindow)
        self.actionOCR_sur_fichiers.setObjectName("actionOCR_sur_fichiers")
        self.actionTrouver_fichiers_sans_texte = QtWidgets.QAction(MainWindow)
        self.actionTrouver_fichiers_sans_texte.setObjectName("actionTrouver_fichiers_sans_texte")
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.statusbar.showMessage("OCR pret")
        self.actionConvertPDFtoJPG = QtWidgets.QAction(MainWindow)
        self.actionConvertPDFtoJPG.setObjectName("Convert_PDF_to_JPG")
        self.actionVerifier_MD5_fichier = QtWidgets.QAction(MainWindow)
        self.actionVerifier_MD5_fichier.setObjectName("actionVerifier_MD5_fichier")	
		
        self.menuFichiers.addAction(self.actionExit)
        self.menuActions.addAction(self.actionAffiche_Fichiers)		
        self.menuActions.addAction(self.actionOCR_sur_fichiers)
        self.menuActions.addAction(self.actionTrouver_fichiers_sans_texte)
        self.menuActions.addAction(self.actionVerifier_MD5_fichier)
        self.menuActions.addAction(self.actionConvertPDFtoJPG)
        self.menubar.addAction(self.menuFichiers.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Chercher"))
        self.menuFichiers.setTitle(_translate("MainWindow", "Fichiers"))
        self.menuActions.setTitle(_translate("MainWindow", "actions"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionAffiche_Fichiers.setText(_translate("MainWindow", "Affiche tous les fichiers"))
        self.actionAffiche_Fichiers.triggered.connect(self.afficheList)		
        self.actionOCR_sur_fichiers.setText(_translate("MainWindow", "OCR sur fichiers"))
        self.actionOCR_sur_fichiers.triggered.connect(self.creationList)
        self.actionTrouver_fichiers_sans_texte.setText(_translate("MainWindow", "Trouver fichiers sans texte"))
        self.actionTrouver_fichiers_sans_texte.triggered.connect(self.checkVide)
        self.actionConvertPDFtoJPG.setText(_translate("MainWindow", "Convertir PDF vers JPG"))
        self.actionConvertPDFtoJPG.triggered.connect(self.convertPDF)
        self.actionVerifier_MD5_fichier.setText(_translate("MainWindow", "verification MD5 des fichiers"))
        self.actionVerifier_MD5_fichier.triggered.connect(self.checkVide)

    def convertPDF(self):
        fichierDejaTrouve=0
        self.listWidget.clear()
        debutFonction = time.clock()
        MD5Traite = open("compte.txt","r").read()
        listFichier = glob.glob("W:\scan_documents\*.pdf")
        for i in listFichier:
            calculMD5 = hashlib.md5(open(i, "rb").read(40000)).hexdigest()
            #print (MD5TraiteOCR.find(calculMD5))
            if MD5Traite.find(calculMD5) == -1:
                all_pages = ImageWand(filename=i, resolution=150)
                open("compte.txt", "a").write(calculMD5 + "\n")
                for t, page in enumerate(all_pages.sequence):
                    QApplication.processEvents()
                    with ImageWand(page) as img:
                        img.format = 'jpg'
                        img.background_color = Color('white')
                        img.alpha_channel = 'remove'

                        image_filename = os.path.splitext(os.path.basename(i))[0]
                        image_filename = '{}-{}.jpg'.format(image_filename, t)
                        self.statusbar.showMessage("traitement du fichier " + image_filename + " ( page " + str(t) + ")")
                        image_filename = os.path.join("W:\scan_documents\\", image_filename)
                        img.save(filename=image_filename)
                        self.listWidget.addItem(os.path.basename(image_filename))
                os.renames(i,os.path.dirname (i)+ "\\fichierPDF\\" + os.path.basename(i))
            else:
                fichierDejaTrouve+=1

        finFonction=time.clock()
        self.statusbar.showMessage("le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(self.listWidget.count()) + " fichiers ont été créé (" + str(fichierDejaTrouve) + " déja trouvés)" )


    def rechercheMot (self, motARechercher):
        debutFonction=time.clock()
        self.listWidget.clear()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse("extractOCR.xml", parser)
        root=tree.getroot()
        for i in root.findall("ElementOCR"):
            if int(i.find("NombreCaractere").text) > 0 :
                if re.search(motARechercher,  i.find("contenuOCR").text, re.IGNORECASE):
                    self.listWidget.addItem(i.find("justeFichier").text)

        finFonction=time.clock()
        self.showdialog (1, "le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(self.listWidget.count()) + " fichiers ont été trouvés " , "", "Recherche de mot", "")								
        self.statusbar.showMessage("le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(self.listWidget.count()) + " fichiers ont été trouvés ")

    def clickMethod(self, index, chemin="traite"):
        posNomFichier=index.data().find(".jpg")
        nomFichier= index.data()[:posNomFichier+4]
        nomFichier="W:\scan_documents\\fichierTraite\\" + nomFichier
        print ("-",nomFichier,"-")
        pixmap = QPixmap(nomFichier)
        self.label.setPixmap(pixmap)
        self.label.setGeometry(QtCore.QRect(450, 30, 800, 950))
        self.label.show()		
		
    def afficheList(self, MainWindow):
        debutFonction=time.clock()
        self.listWidget.clear()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse("extractOCR.xml", parser)	
        root=tree.getroot()
        for i in root.findall("ElementOCR"):	
            self.listWidget.addItem(i.find("justeFichier").text +  " (" + str( i.find("NombreCaractere").text) + ")" )	
            self.listWidget.show()

        finFonction=time.clock()
        #self.showdialog (1, "le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(len(root.getchildren())) + " fichiers ont été trouvés " , "", "Recherche fichiers vides", "")
        self.statusbar.showMessage("le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(len(root.getchildren())) + " fichiers ont été trouvés ")
    def creationList(self, MainWindow):
        retourValeur = self.showdialog (2, "Voulez vous afficher les elements deja trouvés ? ", "", "Recherche fichiers vides", "","YESNOCANCEL")
        print (retourValeur)
        if retourValeur != 4194304:
            self.listWidget.clear()
            debutFonction=time.clock()
            calculMD5 =""
            fichierTrouve=0
            fichierNonTrouve=0
            fichierZero=0
            #MD5Traite = open("compte.txt","r").read()
            MD5TraiteOCR = open("extractOCR.xml","r").read()
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse("extractOCR.xml", parser)
            ElementsOCR= tree.getroot()
            listFichier = glob.glob("W:\scan_documents\*.jpg")
            for i in listFichier:
                QApplication.processEvents()
                self.statusbar.showMessage("Traitement du fichier " + i)
                calculMD5 = hashlib.md5(open(i, "rb").read(40000)).hexdigest()
                if MD5TraiteOCR.find(calculMD5) >= 0:
                    fichierTrouve+=1
                    if retourValeur == 16384:
                        self.listWidget.addItem(os.path.basename(i) + " (deja connu)")
                else:
                    name, ext = os.path.splitext(os.path.basename(i))
                    #print ("Traitement du fichier ", i, " (" , calculMD5, ")")
                    fichierNonTrouve+=1
                    im = Image.open(i)
                    textRecup = ""
                    textRecup = pytesseract.image_to_string(im, lang="fra")
                    if len(textRecup)==0:
                        fichierZero+=1
                        os.renames(i, os.path.dirname (i)+ "\\fichierZero\\" + os.path.basename(i))
                    else:
                        ElementOCR = etree.SubElement(ElementsOCR, "ElementOCR")
                        ElementOCR.set("data-id", calculMD5)
                        extension = etree.SubElement(ElementOCR, "extension")
                        extension.text = ext
                        cheminComplet = etree.SubElement(ElementOCR, "cheminComplet")
                        cheminComplet.text = os.path.dirname(i) + "\\fichierTraite\\" + os.path.basename(i)
                        justeFichier = etree.SubElement(ElementOCR, "justeFichier")
                        justeFichier.text = os.path.basename(i)
                        contenuOCR = etree.SubElement(ElementOCR, "contenuOCR")
                        contenuOCR.text = textRecup.replace("\n","")
                        NombreCaractere = etree.SubElement(ElementOCR, "NombreCaractere")
                        NombreCaractere.text = str(len(contenuOCR.text))
                        self.listWidget.addItem(os.path.basename(i) + " (nouveau, " + NombreCaractere.text + " caracteres)")
                        os.renames(i, os.path.dirname(i) + "\\fichierTraite\\" + os.path.basename(i))

            etree.ElementTree(ElementsOCR).write("extractOCR.xml", pretty_print=True, xml_declaration=True, encoding='iso-8859-1')
            finFonction=time.clock()
            if fichierZero !=0:
                self.showdialog(1, str(fichierZero) + " fichiers vides ont été detectés lors du scan et ils ont été deplacés vers le repertoire fichierZero. Vous pouvez verifier les fichiers et les effacer si besoin","","Fichers vides", "")
            #self.showdialog (1, "le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(fichierNonTrouve) + " nouveaux fichiers ont été trouvés " + " et " + str(fichierTrouve) + " fichiers avaient deja été traités" , "", "OCR sur fichiers", "")
            self.statusbar.showMessage("le traitement est terminé . Il a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes \n " +  str(fichierNonTrouve) + " nouveaux fichiers ont été trouvés " + " et " + str(fichierTrouve) + " fichiers avaient deja été traités" )

    def checkVide(self, MainWindow):
        self.listWidget.clear()	
        debutFonction=time.clock()
        self.listWidget.clear()
        fichierTrouve=0		
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.parse("extractOCR.xml", parser)
        root=tree.getroot()
        for i in root.findall("ElementOCR"):		
            print ("nb car " , i.find("NombreCaractere").text)
            if int(i.find("NombreCaractere").text) == 0 :
                fichierTrouve+=1
                self.listWidget.addItem(i.find("justeFichier").text)				
				
        finFonction=time.clock()
        #self.showdialog (1, "le traitement a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes et " + str (fichierTrouve) + " fichiers vides ont été trouvés", "", "Recherche fichiers vides", "")
        self.statusbar.showMessage("le traitement est terminé et il a duré " + str(round (finFonction - debutFonction,2)).replace (".",",") + " secondes et " + str (fichierTrouve) + " fichiers vides ont été trouvés")

    def showdialog(self, icone, textBox, informativeBox, titre, detail, bouton="OK"):

        msg = QMessageBox()
        if icone == 1:
            msg.setIcon(QMessageBox.Information)
        elif icone == 2:
            msg.setIcon(QMessageBox.Question)
        elif icone == 3:
            msg.setIcon(QMessageBox.Warning)
        elif icone == 4:
            msg.setIcon(QMessageBox.Critical)			
        else:
            msg.setIcon(QMessageBox.NoIcon)      

        msg.setText(textBox)
		
        if informativeBox != "":
            msg.setInformativeText(informativeBox)
			
        msg.setWindowTitle(titre)
		
        if detail != "":
            msg.setDetailedText(detail)

        if 	bouton == "YESNOCANCEL":
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes | QMessageBox.Cancel)
        elif bouton == "YESNO":
            msg.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        else:
            msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()
        # 16384 est pour YES, 65536 pour NO et 4194304 pour cancel
        return  retval
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

