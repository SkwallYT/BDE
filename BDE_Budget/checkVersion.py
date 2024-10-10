#####################################################
# Author : DETUNCQ Valentin                         #
#                                                   #
# Check la version du programme, si obsolete, update#
#####################################################

import requests, shutil, os

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
        if elt == 'main.py':
            url =

def version_control():
    pass

if __name__ == '__main__' :
    if not check_file()[0]:

    URL = "https://www.stackoverflow.com/favicon.ico"
    response = requests.get(URL)
    if 'file_exist' == False:
        pass
    if True :
        version_control()