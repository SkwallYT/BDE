#####################################################
# Author : DETUNCQ Valentin                         #
#                                                   #
# Check la version du programme, si obsolete, update#
#####################################################

import requests, shutil, os

# Liens vers les fichiers git
version_url = 'https://raw.githubusercontent.com/SkwallYT/BDE/refs/heads/main/BDE_Budget/Version'
changelog_url = 'https://raw.githubusercontent.com/SkwallYT/BDE/refs/heads/main/BDE_Budget/FileChangelog'
getBudgetUI_url = 'https://raw.githubusercontent.com/SkwallYT/BDE/refs/heads/main/BDE_Budget/getBudgetUI.py'
main_url = 'https://raw.githubusercontent.com/SkwallYT/BDE/refs/heads/main/BDE_Budget/main.py'

def check_file():
    """
    Permet de verifier l'integrite des fichiers de l'application

    :return: bool True si tous les fichiers sont good, sinon False
    """
    l = ['main.py', 'getBudgetUI.py', 'Version', 'FileChangelog']
    ret_l = []
    ret_bool = True
    for elt in l:
        if not os.path.exists(elt):
            ret_bool =  False
            ret_l.append(elt)
    return ret_bool, ret_l

def download_file(list_files):
    """
    Permet de telecharger les fichiers manquant dant la liste list_files

    :param list_files: liste des fichiers
    :return: bool True si tous les fichiers sont good, sinon False
    """
    for elt in list_files:

        try:
            if elt == 'main.py':
                reponse = requests.get(main_url)
                with open(elt, mode='wb') as f:
                    f.write(reponse.content)
                    f.close()

            if elt == 'getBudgetUI.py':
                reponse = requests.get(getBudgetUI_url)
                with open(elt, mode='wb') as f:
                    f.write(reponse.content)
                    f.close()

            if elt == 'Version':
                reponse = requests.get(version_url)
                with open(elt, mode='wb') as f:
                    f.write(reponse.content)
                    f.close()

            if elt == 'FileChangelog':
                reponse = requests.get(changelog_url)
                with open(elt, mode='wb') as f:
                    f.write(reponse.content)
                    f.close()

        except Exception as e:
            print(e)
            return False

    return True

def version_control():

    with open('Version', 'r') as f:
        version = f.read().strip()

    if version != requests.get(version_url).content:
        os.remove('FileChangelog')
        download_file(['FileChangelog'])
        with open('FileChangelog', 'r') as f:
            a = f.readlines()
            f.close()

        file_list = []

        for elt in a:
            file_list.append(elt[:-1])

        for elt2 in file_list:
             os.remove(elt2)

        os.remove('Version')
        file_list.append('Version')
        download_file(file_list)

if __name__ == '__main__' :
    if not check_file()[0]:
        download_file(check_file()[1])

    version_control()
