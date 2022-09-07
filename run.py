import argparse
import logging
from os import getenv, mkdir
from os.path import join
from shutil import rmtree

from hdx.api.configuration import Configuration
from hdx.facades.keyword_arguments import facade
from hdx.utilities.downloader import Download
from hdx.utilities.easy_logging import setup_logging
from hdx.utilities.retriever import Retrieve
from iati.main import start

setup_logging()
logger = logging.getLogger()


VERSION = 1.0


def parse_args():
    parser = argparse.ArgumentParser(description="IATI downloader")
    parser.add_argument("-ua", "--user_agent", default=None, help="user agent")
    parser.add_argument("-pp", "--preprefix", default=None, help="preprefix")
    parser.add_argument("-od", "--output_dir", default="output", help="Output folder")
    parser.add_argument(
        "-sd", "--saved_dir", default="saved_data", help="Saved data folder"
    )
    parser.add_argument(
        "-sv", "--save", default=False, action="store_true", help="Save downloaded data"
    )
    parser.add_argument(
        "-usv", "--use_saved", default=False, action="store_true", help="Use saved data"
    )
    parser.add_argument(
        "-dp",
        "--dportal_params",
        default="",
        help="Parameters for DPortal query (eg. limit X, offset Y)",
    )
    parser.add_argument(
        "-wh", "--what", default="pakistanfloods", help="What to run eg. covid, ebola"
    )
    args = parser.parse_args()
    return args


def main(
    output_dir,
    saved_dir,
    save,
    use_saved,
    dportal_params,
    whattorun,
    **ignore,
):
    logger.info(f"##### hdx-scraper-iati-pakistanfloods version {VERSION:.1f} ####")
    configuration = Configuration.read()
    output_dir = f"{output_dir}_{whattorun}"
    rmtree(output_dir, ignore_errors=True)
    mkdir(output_dir)
    with Download() as downloader:
        retriever = Retrieve(
            downloader,
            configuration["fallback_dir"],
            f"{saved_dir}_{whattorun}",
            output_dir,
            save,
            use_saved,
        )
        start(
            configuration,
            retriever,
            dportal_params,
            whattorun,
        )


if __name__ == "__main__":
    args = parse_args()
    user_agent = args.user_agent
    if user_agent is None:
        user_agent = getenv("USER_AGENT")
        if user_agent is None:
            user_agent = "hdx-scraper-iati-downloadonly"
    preprefix = args.preprefix
    if preprefix is None:
        preprefix = getenv("PREPREFIX")
    facade(
        main,
        hdx_read_only=True,
        user_agent=user_agent,
        preprefix=preprefix,
        project_config_yaml=join("config", "project_configuration.yml"),
        output_dir=args.output_dir,
        saved_dir=args.saved_dir,
        save=args.save,
        use_saved=args.use_saved,
        dportal_params=args.dportal_params,
        whattorun=args.what,
    )
