import sys
import os

input_path = sys.argv[1]
output_path = "dedicated_server_mods_setup.lua"

print(input_path)

def get_mod_id_from_path(mod_path):
    dir_name = os.path.basename(mod_path)
    id = dir_name[9:]
    return id


def get_all_mods(mods_path):
    mod_directories = os.listdir(mods_path)
    mod_directories = list(filter(lambda x: "workshop-" in x, mod_directories))
    for directory in mod_directories:
        mod = None
        try:
            mod = get_mod_name_and_id(f"{mods_path}/{directory}")
        except Exception as e:
            print(e)
            continue
        yield mod


def get_mod_name_and_id(mod_path):
    mod_info_path = f"{mod_path}/modinfo.lua"
    with open(mod_info_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("name = "):
                mod_name = line[8:-2]
                return (mod_path, mod_name)

    raise Exception(
        f"Could not find the name of the mod in file '{mod_info_path}'")


def write_dedicated_server_mods_setup_lua(mods, output_path):
    with open(output_path, "w") as f:
        for mod_path, name in mods:
            id = get_mod_id_from_path(mod_path)
            f.write(f"--#{name}\n")
            f.write(f"ServerModSetup(\"{id}\")\n")
    file_name = os.path.basename(output_path)
    print(f"File '{file_name}' created succesfully!")


l = sorted(list(get_all_mods(input_path)))
write_dedicated_server_mods_setup_lua(l, output_path)