import pycurl
from io import BytesIO
import os

program_version = "v0.1.0"

asset_root = "https://explore.gethopscotch.com/"
game_root = "https://explore.gethopscotch.com/e/"

start_text = """/================================
Hopscotch Game Downloader""" + "\n" + program_version + """
Created by FarawayDrip30
https://farawaydrip30.co.uk/"""
option_text = """/--------------------------------
Select Option:
1. Download Game
2. Download HopscotchData
3. Exit"""

def download_read_file(url):
    # Get HTML data
    buffer = BytesIO()
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)
    c.perform()
    c.close()

    # Parse HTML data to string
    body = buffer.getvalue()
    string = body.decode("utf-8")

    return string

def download_file(url, save_as):
    if len(url) > 0 and len(save_as) > 0:
        print("Downloading \"" + url + "\", Saving As \"" + save_as + "\"")

        buffer = BytesIO()
        c = pycurl.Curl()
        c.setopt(c.URL, url)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()

        f = open(save_as, "wb")
        f.write(buffer.getbuffer())

def list_to_string(list_path):
    list_file = open(list_path, "r")
    list_string = list_file.read()
    list_file.close()

    list_entries = list_string.split(";")
    for i in range(len(list_entries)):
        list_entries[i] = list_entries[i].strip()
        list_entries[i] = list_entries[i].replace(" ", "")
    
    return list_entries

def split_list_entries_into_2_arrays(list_entries, splitter, array1, array2, duplicate_value_if_no_splitter):
    for entry in list_entries:
        if splitter in entry:
            split_list = entry.split(splitter)
            array1.append(split_list[0])
            array2.append(split_list[1])
        else:
            array1.append(entry)
            if duplicate_value_if_no_splitter:
                array2.append(entry)
            else:
                array2.append("")

def download_from_list(list_path, url_root, save_as_root):
    list_entries = list_to_string(list_path)

    urls = []
    save_ases = []
    split_list_entries_into_2_arrays(list_entries, ">", urls, save_ases, True)

    for i in range(len(urls)):
        if len(urls[i]) > 0 and len(save_ases[i]) > 0:
            download_file(url_root + urls[i], save_as_root + save_ases[i])


def replace_from_list(list_path, original_string):
    string = original_string[:]

    list_entries = list_to_string(list_path)

    original_substrings = []
    replacement_substrings = []
    split_list_entries_into_2_arrays(list_entries, ">", original_substrings, replacement_substrings, True)

    for i in range(len(original_substrings)):
        if len(original_substrings[i]) > 0 and len(replacement_substrings[i]) > 0:
            print("Replacing \"" + original_substrings[i] + "\" Substring with \"" + replacement_substrings[i] + "\" Substring.")
            string = string.replace(original_substrings[i], replacement_substrings[i])
    
    return string

def save_string(file_name, _string, _encoding):
    print("Saving \"" + file_name + "\" Using +\"" + _encoding + "\" Encoding")
    output_file = open(file_name, "w", encoding=_encoding)
    output_file.write(_string)
    output_file.close()

def download_game():
    game_code = input("Input Game Code: ").strip()
    game_name = input("Enter the Name of Your Game: ").strip()

    game_index = game_root + game_code

    html_string = download_read_file(game_index)

    # Download thumbnail image
    download_file("https://s3.amazonaws.com/hopscotch-cover-images/production/" + game_code + ".png", game_name + ".png")

    # Replace everything with downloaded local versions
    html_string = replace_from_list("replacements.txt", html_string)

    # Thumbnail image replace
    print("Replacing \""+"https://s3.amazonaws.com/hopscotch-cover-images/production/"+game_code+".png"+"\" Substring with \""+ game_name+".png"+"\" Substring.")
    html_string = html_string.replace("https://s3.amazonaws.com/hopscotch-cover-images/production/" + game_code + ".png", game_name + ".png")

    # Save HTML
    save_string(game_name + ".html", html_string, "utf-8")
    

required_folders = [
    "HopscotchData",
    "HopscotchData/fonts",
    "HopscotchData/page-scripts",
    "HopscotchData/player",
    "HopscotchData/stylesheets",
]
def download_hopscotch_data():
    # Make required folders
    for folder in required_folders:
        if not os.path.exists(folder):
            print("Creating Folder \"" + folder + "\"")
            os.makedirs(folder)

    download_from_list("downloads_hopscotchdata_relative.txt", asset_root, "HopscotchData/")
    download_from_list("downloads_hopscotchdata_absolute.txt", "", "HopscotchData/")

    # Get Main.js and remove it trying to load amplitude.js
    mainjs_string = download_read_file(asset_root + "main.js")
    print("Patching \"main.js\"")
    # Find function that loads amplitude
    load_amplitude_func_start = mainjs_string.find("!function")
    # Find code in function that uses amplitude
    send_amplitude_func_start = mainjs_string.find("sendEvent")
    send_amplitude_code_start = mainjs_string.find("amplitude", send_amplitude_func_start)
    # Add comments
    mainjs_string = mainjs_string[:load_amplitude_func_start] + "//" + mainjs_string[load_amplitude_func_start:send_amplitude_code_start] + "//" + mainjs_string[send_amplitude_code_start:]
    # Save main.js
    save_string("HopscotchData/main.js", mainjs_string, "utf-8")

    print("Successfully Downloaded HopscotchData!")


if __name__ == "__main__":
    print(start_text)
    while True:
        print(option_text)
        option_chosen = input(">")
        
        if option_chosen[0] == "1":
            print("Download Game")
            download_game()
        elif option_chosen[0] == "2":
            print("Download HopscotchData")
            download_hopscotch_data()
        elif option_chosen[0] == "3":
            print("Exit")
            break
        else:
            print("Unknown Option Entered")
