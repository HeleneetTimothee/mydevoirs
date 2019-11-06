import os


base = os.environ["MYDEVOIRS_BASE_DIR"]

"""
On dispatch les datas sous la forme :
    type_nom : "nom_du_fichier"
qui donnera le path : racine_de_base/data/genres/nom_du_fichier

Permet :
- de gerer le root pour  dev et pyinstaller
- utiliser des variables  pour désigner les datas
"""

DATAS = {
    "icon_precedant": "chevron-left.png",
    "icon_suivant": "chevron-right.png",
    "icon_today": "calendar.png",
}


def get_datas():
    res = {}
    for k, v in DATAS.items():

        genre, nom = k.split("_")
        res[k] = os.path.join(base, "data", genre + "s", v)
    return res


datas = get_datas()