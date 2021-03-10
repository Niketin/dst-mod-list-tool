import os
import argparse
import platform
import getpass

dsms_lua_file_name = "dedicated_server_mods_setup.lua"
mo_lua_file_name = "modoverrides.lua"
description = f"""Mod list generator for Don't Starve Together Dedicated Server.

It automatically generates '{mo_lua_file_name}' and '{dsms_lua_file_name}' lists containing the mods that are currently installed in the Don't Starve Together game.
Normally the files are created by hand.
This generator should make the job a lot faster.
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


def write_modoverrides_lua(mods, output_path):
    with open(output_path, "w") as f:
        f.write("return {\n")
        for i, (mod_path, name) in enumerate(mods):
            id = get_mod_id_from_path(mod_path)
            f.write(f"--#{name}\n")
            period_if_not_last = "," if i < len(mods) - 1 else ""
            f.write(
                f"[\"workshop-{id}\"] = {{ enabled = true }}{period_if_not_last}\n")
        f.write("}")
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
        description=description)

    path_group = parser.add_mutually_exclusive_group(required=True)
    path_group.add_argument(
        "--dst-path", help="Path to Don't Starve Together installation folder.")
    path_group.add_argument(
        "--auto", action="store_true", help="Automatically determine the Don't Starve Together installation folder.")
    args = parser.parse_args()

    dst_path = None
    if args.dst_path:
        dst_path = args.dst_path
    elif args.auto:
        dst_path = find_dst_directory()
    else:
        raise Exception("test")

    mods_path = os.path.join(dst_path, 'mods')
    mods = sorted(list(get_all_mods(mods_path)))
    print(f"Generated {len(mods)} items.")

    write_dedicated_server_mods_setup_lua(mods, dsms_lua_file_name)
    write_modoverrides_lua(mods, mo_lua_file_name)


if __name__ == "__main__":
    main()
