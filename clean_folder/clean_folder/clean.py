import sys
import os
import shutil
import zipfile

filepath = ""

lat_letters = "abcdefghijklmnopqrstuvwxyz1234567890"

translit = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "yo",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "j",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "h",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ь": "'",
    "ъ": "''",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya"
}

files_groups = {
    "images": [],
    "video": [],
    "documents": [],
    "audio": [],
    "archives": [],
    "others": []
}

known_extensions = {
    "images": ["jpeg", "png", "jpg", "svg"],
    "video": ["avi", "mp4", "mov", "mkv"],
    "documents": ["doc", "docx", "txt", "pdf", "xlsx", "pptx"],
    "audio": ["mp3", "ogg", "wav", "amr"],
    "archives": ["zip", "gz", "tar"]
}

white_list_dir = ["images", "video", "documents", "audio", "archives"]
known_extensions_in_folder = []
unknown_extensions_in_folder = []


def check_folder(path=""):
    if path.split("\\")[-1] not in white_list_dir:
        for item in os.listdir(path):
            if os.path.isfile(os.path.join(path, item)):
                if item.split(".")[-1] in known_extensions["images"]:
                    if item.split(".")[-1] not in known_extensions_in_folder:
                        known_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["images"].append(os.path.join(path, item))
                elif item.split(".")[-1] in known_extensions["video"]:
                    if item.split(".")[-1] not in known_extensions_in_folder:
                        known_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["video"].append(os.path.join(path, item))
                elif item.split(".")[-1] in known_extensions["documents"]:
                    if item.split(".")[-1] not in known_extensions_in_folder:
                        known_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["documents"].append(os.path.join(path, item))
                elif item.split(".")[-1] in known_extensions["audio"]:
                    if item.split(".")[-1] not in known_extensions_in_folder:
                        known_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["audio"].append(os.path.join(path, item))
                elif item.split(".")[-1] in known_extensions["archives"]:
                    if item.split(".")[-1] not in known_extensions_in_folder:
                        known_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["archives"].append(os.path.join(path, item))
                else:
                    if item.split(".")[-1] not in unknown_extensions_in_folder:
                        unknown_extensions_in_folder.append(item.split(".")[-1])
                    files_groups["others"].append(os.path.join(path, item))
            else:
                check_folder(os.path.join(path, item))


def normalize(filename):
    translit_filename = ""
    for letter in "".join(filename.split(".")[:-1]):
        if letter.lower() in translit.keys():
            if letter.islower():
                cur_letter = translit[letter]
            else:
                cur_letter = translit[letter.lower()].upper()
        elif letter.lower() not in lat_letters:
            cur_letter = "_"
        else:
            cur_letter = letter
        translit_filename += cur_letter
    translit_filename += "." + filename.split(".")[-1]
    return translit_filename


def images(imgs):
    for img in imgs:
        new_filename = normalize(img.split("\\")[-1])
        if not os.path.exists(os.path.join(filepath, "images")):
            os.mkdir(os.path.join(filepath, "images"))
        shutil.move(img, os.path.join(filepath, "images", new_filename))


def documents(docs):
    for doc in docs:
        new_filename = normalize(doc.split("\\")[-1])
        if not os.path.exists(os.path.join(filepath, "documents")):
            os.mkdir(os.path.join(filepath, "documents"))
        shutil.move(doc, os.path.join(filepath, "documents", new_filename))


def audio(musics):
    for music in musics:
        new_filename = normalize(music.split("\\")[-1])
        if not os.path.exists(os.path.join(filepath, "audio")):
            os.mkdir(os.path.join(filepath, "audio"))
        shutil.move(music, os.path.join(filepath, "audio", new_filename))


def video(videos):
    for vid in videos:
        new_filename = normalize(vid.split("\\")[-1])
        if not os.path.exists(os.path.join(filepath, "video")):
            os.mkdir(os.path.join(filepath, "video"))
        shutil.move(vid, os.path.join(filepath, "video", new_filename))


def archives(archive):
    for arc in archive:
        new_filename = normalize(arc.split("\\")[-1])
        new_filename = "".join(new_filename.split(".")[:-1])
        zip_file = zipfile.ZipFile(arc)
        if not os.path.exists(os.path.join(filepath, "archives")):
            os.mkdir(os.path.join(filepath, "archives"))
        zip_file.extractall(os.path.join(filepath, "archives", new_filename))


def main():
    print(sys.argv)
    if len(sys.argv) > 1:
        global filepath
        filepath = sys.argv[1]
        check_folder(filepath)
    else:
        print("Filepath cannot be empty")
    for key in files_groups:
        print(f"{key}:")
        for item in files_groups[key]:
            print("    ", item)
    print("_" * 45)
    print("Известные расширения найденные в директории:")
    print("    ", ", ".join(known_extensions_in_folder))
    print("_" * 45)
    print("Известные расширения найденные в директории:")
    print("    ", ", ".join(unknown_extensions_in_folder))
    images(files_groups["images"])
    documents(files_groups["documents"])
    audio(files_groups["audio"])
    video(files_groups["video"])
    archives(files_groups["archives"])
