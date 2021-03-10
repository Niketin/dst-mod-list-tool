import os
import argparse
import platform
import getpass

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


def find_dst_directory():
    if platform.system() != "Linux":
        raise Exception("Unsupported feature on non-Linux machine.")
    user = getpass.getuser()
    path = f"/home/{user}/.steam/steam/steamapps/common/Don't Starve Together"
    if not os.path.exists(path):
        raise Exception("DST path could not be found.")
    return path


def main():
    parser = argparse.ArgumentParser(
        description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument(
        "--dst-path", help="Path to Don't Starve Together installation folder.")
    parser.add_argument(
        "--output-path", help="Override the output file path. A new file is automatically created. If the file already exists, the result will be appended to the end of the file.")
    args = parser.parse_args()

    output_path = default_output_path
    if args.output_path:
        output_path = args.output_path

    dst_path = None
    if args.dst_path:
        dst_path = args.dst_path
    else:
        try:
            dst_path = find_dst_directory()
        except Exception as e:
            print(e)

    mods = sorted(list(get_all_mods(f"{dst_path}/mods")))
    print(f"Generated {len(mods)} items.")
    write_dedicated_server_mods_setup_lua(mods, output_path)


if __name__ == "__main__":
    main()
