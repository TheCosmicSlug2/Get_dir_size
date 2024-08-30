import os
from time import perf_counter

def is_file(path: str) -> bool:
    return os.path.isfile(path)

def is_dir(path: str) -> bool:
    return os.path.isdir(path)


def check_entries(main_dir_path: str, list_paths: list) -> int:
    """Collecte les chemins des fichiers pour des petits dossiers"""
    try:
        entries = os.listdir(main_dir_path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"{e}")
        return 0

    for entry in entries:
        path = os.path.join(main_dir_path, entry)
        if is_file(path):
            list_paths.append(path)
        elif is_dir(path):
            check_entries(path, list_paths)

def check_size(liste: list) -> int:
    """Calcule la taille des fichiers d'une liste"""
    total_size = 0
    for path in liste:
        try:
            total_size += os.path.getsize(path)
        except (FileNotFoundError, PermissionError) as e:
            print(f"{e}")
    return total_size





def list_method(main_path: str, details: bool) -> int:
    list_paths = []
    time1 = perf_counter()
    check_entries(main_path, list_paths)
    total_size = check_size(list_paths)
    formatted_total_size = format(total_size, '_').replace('_', ' ')
    if details:
        print(f"=> \"{main_path}\": \n"
              f"{formatted_total_size} octets ({len(list_paths)} fichiers)\n\n"
              f"en : {round(perf_counter() - time1, 5)} secondes")
    else:
        print(f"=> \"{main_path}\" : {formatted_total_size} octets ({len(list_paths)} fichiers)")
    return total_size

"""
# On va pas utiliser cette merde qui marche une fois sur 2

def check_entries_get_size(main_dir_path: str) -> int:
    #Calculer la taille d'un dossier et de ses sous-dossiers
    dir_size = 0
    try:
        entries = os.listdir(main_dir_path)
    except (FileNotFoundError, PermissionError) as e:
        print(f"Erreur d'accès au répertoire {main_dir_path}: {e}")
        return dir_size

    for entry in entries:
        path = os.path.join(main_dir_path, entry)
        if is_file(path):
            try:
                dir_size += os.path.getsize(path)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Erreur d'accès au fichier {path}: {e}")
        elif is_dir(path):
            dir_size += check_entries_get_size(path)
    return dir_size

def raw_method(main_path, details):
    time1 = perf_counter()
    total_size = check_entries_get_size(main_path)
    formatted_total_size = format(total_size, '_').replace('_', ' ')
    if details:
        print(f"Taille de tous les fichiers du dossier \"{main_path}\": \n"
              f"{formatted_total_size} octets\n\n"
              f"en : {round(perf_counter() - time1, 5)} secondes")
    else:
        print(f"\"{main_path}\" : {formatted_total_size} octets")
    return total_size
"""


def analyse_one_dir() -> None:
    default_path = input("\nQuel dossier voulez-vous analyser ? : \n >> ").strip()

    list_method(default_path, details=True)


def analyse_all_dirs_in_dir() -> None:
    default_path = input("\nQuel dossier voulez-vous analyser ? : \n >> ").strip()

    list_analyse_paths = os.listdir(default_path)
    dict_all_sizes = {}
    for directory_name in list_analyse_paths:
        path = f"{default_path}\\{directory_name}"
        if is_dir(path):
            dict_all_sizes[directory_name] = list_method(f"{path}", details=False)

    total_size = sum(dict_all_sizes.values())
    print(f"\n\nVisualisation des tailles dans \"{default_path}\" ({format(total_size, '_').replace('_', ' ')} octets) : \n")
    for path, size in dict_all_sizes.items():
        percentage = round(size/total_size * 100)
        barre_pourcentage = percentage * "|"
        print(f"{barre_pourcentage}~{percentage}% : {path}")



if __name__ == "__main__":
    running = True
    while running:
        if input("\nAnalyser en détails ? (o/n) : \n >> ") == "o":
            analyse_all_dirs_in_dir()
        else:
            analyse_one_dir()

        if input("\nRefaire (o/n) : \n >> ") == "n":
            running = False
