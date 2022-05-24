import argparse


def set_default_options_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument(
        "-d", "--dest_folder", type=str, default='',
        help="Path to the directory with the parsing results"
    )

    parser.add_argument(
        "-j", "--json_path", type=str, default='',
        help="Specify your path to * .json file with results"
    )

    parser.add_argument(
        "-si", "--skip_imgs",
        default=False, type=bool,
        help="Do not download images"
    )

    parser.add_argument(
        "-st", "--skip_txt",
        default=False, type=bool,
        help="Do not download text"
    )

    return parser
