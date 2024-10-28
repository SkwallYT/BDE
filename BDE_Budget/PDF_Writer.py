###########################################################
# Author : DETUNCQ Valentin                               #
#                                                         #
# ecrire le compte rendu du compte et le mettre en pdf    #
###########################################################

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
import os

def generer_pdf_compte_rendu(nom_fichier, titre, montant_total, transactions):
    # Création du document PDF

    if not os.path.exists("Compte_Rendu/"):
        os.makedirs("Compte_Rendu/")

    if os.path.exists("Compte_Rendu/" + nom_fichier):
        os.remove("Compte_Rendu/" + nom_fichier)

    doc = SimpleDocTemplate("Compte_Rendu/" + nom_fichier, pagesize=A4)
    elements = []

    # Style du document
    styles = getSampleStyleSheet()
    style_titre = styles['Heading1']
    style_texte = styles['BodyText']

    # Ajouter la date et l'heure
    date_heure = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    elements.append(Paragraph(f"Date de réalisation : {date_heure}", style_texte))
    elements.append(Spacer(1, 0.5 * cm))

    # Titre du rapport
    elements.append(Paragraph(titre, style_titre))
    elements.append(Spacer(1, 0.5 * cm))

    # Montant total du compte
    elements.append(Paragraph(f"Montant actuel du compte : {montant_total:.2f}€", style_texte))
    elements.append(Spacer(1, 0.5 * cm))

    # Table des transactions
    if transactions:
        # En-têtes de colonnes
        data = [["Date", "Montant (€)", "Raison", "Personne"]]
        # Ajout des transactions dans le tableau
        for transaction in transactions:
            data.append([
                transaction["date"],
                f"{transaction['montant']:.2f}",
                transaction["raison"],
                transaction["personne"]
            ])

        # Style de la table
        table = Table(data, colWidths=[4*cm, 3*cm, 6*cm, 4*cm])
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('FONTSIZE', (0, 1), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke)
        ])
        table.setStyle(style)
        elements.append(table)

    # Générer le PDF
    doc.build(elements)
    print(f"PDF généré : {nom_fichier}")

    return True, f"PDF généré : {nom_fichier}"