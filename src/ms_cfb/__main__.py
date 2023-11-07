import argparse
import os
import uuid
import yaml
from pathlib import Path
from ms_cfb.ole_file import OleFile
from ms_cfb.Models.Directories.directory import Directory
from ms_cfb.Models.Directories.root_directory import RootDirectory
from ms_cfb.Models.Directories.storage_directory import StorageDirectory
from ms_cfb.Models.Directories.stream_directory import StreamDirectory
from ms_dtyp.filetime import Filetime


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("directory",
                        help="The input or output directory.")
    parser.add_argument("-c", "--create", action="store_true",
                        help="Create an OLE file from a directory.")
    parser.add_argument("-l", "--list", action="store_true",
                        help="Display metadata on the OLE file and list the files that it contains.")
    parser.add_argument("-x", "--extract", action="store_true",
                        help="Extract files from an OLE file to a directory.")
    parser.add_argument("-v", "--version", type=int, choices=[3, 4],
                        help="The OLE version to use.")
    parser.add_argument("-f", "--file",
                        help="The input or output bin file name")
    parser.add_argument("-X", "--extra",
                        help="Path to exta settings yml file.")
    args = parser.parse_args()
    if args.create:
        main_create(args)
    if args.extract:
        main_extract(args)
    if args.list:
        main_list(args)


def main_create(args: argparse.Namespace) -> None:
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
    ole_file.create_file(args.file)


def main_extract(args: argparse.Namespace) -> None:
    pass


def main_list(args: argparse.Namespace) -> None:
    pass


def update_attributes(dir: 'Directory', conf: dict) -> None:
    if "modified" in conf:
        datetime = Filetime.fromisoformat(conf["modified"])
        dir.set_modified(datetime)
    if "created" in conf:
        datetime = Filetime.fromisoformat(conf["created"])
        dir.set_created(datetime)
    if "clsid" in conf:
        dir.set_clsid(uuid.UUID(conf["clsid"]))
    if "flags" in conf:
        dir.set_flags(conf["flags"])


def create_storage(direntry: os.DirEntry,
                   directories: dict) -> StorageDirectory:
    dir = StorageDirectory(direntry.name)
    obj = os.scandir(direntry.path)
    for entry in obj:
        if entry.is_dir():
            dir.add_directory(create_storage(entry, directories))
        else:
            stem = Path(entry.name).stem
            stream = StreamDirectory(stem, entry.path)
            dir.add_directory(stream)
    mod_time = Filetime.fromtimestamp(os.stat(direntry.path).st_mtime)
    dir.set_modified(mod_time)
    if direntry.name in directories:
        dir_config = directories[direntry.name]
        update_attributes(dir, dir_config)
    return dir


if __name__ == '__main__':
    main()
