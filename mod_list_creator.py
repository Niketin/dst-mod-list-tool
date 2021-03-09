import os
import argparse

default_output_path = "dedicated_server_mods_setup.lua"
description = f"""Mod list generator for Don't Starve Together Dedicated Server.
  By default it outputs the file '{default_output_path} to the current directory.'
"""


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
    with open(output_path, "a") as f:
        for mod_path, name in mods:
            id = get_mod_id_from_path(mod_path)
            f.write(f"--#{name}\n")
            f.write(f"ServerModSetup(\"{id}\")\n")
    file_name = os.path.basename(output_path)
    print(f"File '{file_name}' created succesfully!")


def main():
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "mods_path", help="Path to Don't Starve Together mods folder")
    parser.add_argument(
        "--output-path", help="Override the output file path. A new file is automatically created. If the file already exists, the result will be appended to the end of the file.")
    args = parser.parse_args()

    output_path = default_output_path
    if args.output_path:
        output_path = args.output_path

    mods_path = None
    if args.mods_path:
        mods_path = args.mods_path
    else:
        # TODO find mods path automatically. 'mods_path' needs to be optional argument.
        pass

    mods = sorted(list(get_all_mods(mods_path)))
    print(f"Generated {len(mods)} items.")
    write_dedicated_server_mods_setup_lua(mods, output_path)



if __name__ == "__main__":
    main()
