import argparse
import os
import yaml
from ms_cfb.ole_file import OleFile


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The input or output directory.")
    parser.add_argument("-c", "--create", action="store_true",
                        help="Create an OLE file from a directory.")
    parser.add_argument("-x", "--extract", action="store_true",
                        help="Extract files from an OLE file to a directory.")
    parser.add_argument("-v", "--version", type=int, choices=[3, 4],
                        help="The OLE version to use.")
    parser.add_argument("-f", "--file",
                        help="The input or output bin file name")
    parser.add_argument("-X", "--extra",
                        help="Path to exta settings yml file.")
    args = parser.parse_args()
    ole_file = OleFile()
    if args.version == 4:
        ole_file.set_version(4)
    config = {"directories": {}}
    if args.extra is not None and os.path.isfile(args.extra):
        stream = open(args.extra, 'r')
        config = yaml.safe_load(stream)
    new_config = config["directories"]

    root = RootDirectory()
    obj = os.scandir(args.directory)
    for entry in obj:
        if entry.is_dir():
            root.add_directory(create_storage(entry, new_config))
        else:
            dir = StreamDirectory(entry.name, entry.path)
            root.add_directory(dir)
    mod_time = os.stat(args.directory).st_mtime
    ft = Filetime.fromtimestamp(mod_time)
    root.set_modified(ft)
    if "." in new_config:
        dir_config = new_config["."]
        update_attributes(root, dir_config)
    ole_file.set_root_directory(root)
    ole_file.create_file(args.output)


if __name__ == '__main__':
    main()
