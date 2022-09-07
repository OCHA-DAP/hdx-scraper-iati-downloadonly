import logging
from urllib.parse import quote


logger = logging.getLogger(__name__)


def retrieve_dportal(dportal_configuration, whattorun, retriever, dportal_params=""):
    """
    Downloads activity data from D-Portal. Filters them and returns a
    list of activities.
    """
    filename = dportal_configuration["filename"]
    url = dportal_configuration["url"] % quote(
        dportal_configuration[f"{whattorun}_query"].format(dportal_params)
    )
    return filename, retriever.download_file(
        url, filename, "D-Portal activities", False
    )


def start(
    configuration,
    retriever,
    dportal_params,
    whattorun,
):
    retrieve_dportal(
        configuration, whattorun, retriever, dportal_params
    )
