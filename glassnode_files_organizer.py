from os import listdir
from os.path import isfile, join
import os
import json
import re
from pprint import pprint
import pandas as pd
import os
import errno




def glassnode_files_organizer():
    
    def make_sure_path_exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

    mypath = "/home/locsta/Documents/Glassnode 4"
    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    json_files_to_convert = [mypath + "/" + f for f in files if f.endswith(".json")]
    for json_file_path in json_files_to_convert:
        with open(json_file_path) as json_file:
            data = json.load(json_file)
            df = pd.DataFrame(data)
            df.to_csv(json_file_path.replace(".json", "(8).csv"),index=False)
            os.remove(json_file_path)

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # Remove duplicates files
    for i in range(10):
        [os.remove(mypath + "/" + f) for f in files if f"({i})" in f]

    files = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    # quit()
    count = 0
    with open('/home/locsta/Documents/Glassnode 4 (jsons)/files_tree.json') as json_file:
        data = json.load(json_file)
        categories = data.keys()
        for category in categories:
            sections = data[category].keys()
            for section in sections:
                data_names = data[category][section]
                # print(data_names)
                for name in data_names:
                    try:
                        tier = name.split(" - ")[0]
                        formatted_name = name.split(" - ")[1].lower().replace(" ", "-")
                        if (formatted_name + ".csv") in files:
                            print(category)
                            print(section, f"- ({tier})")
                            # print(formatted_name)
                            # quit()
                            make_sure_path_exists(f"/home/locsta/Documents/GlassNodeStudio/{category}/{section}")
                            os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
                    except:
                        pass

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    glassnode_files_organizer()