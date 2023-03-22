import pytz
import logging
from typing import NamedTuple
import requests
import traceback
from datetime import datetime

from .parser import process_calendar
from ..models import DownloadReport

logger = logging.getLogger(__name__)
tz = pytz.timezone("Asia/Jerusalem")


class ResourceTuple(NamedTuple):
    id: str
    name: str
    when_created: datetime
    mimetype: str
    url: str
    package_id: str


def get_resource(resource_id: str, website: str):
    resource_show = f"{website}/api/3/action/resource_show"
    res = requests.get(resource_show, params={"id": resource_id})
    res.raise_for_status()
    j = res.json()
    result = j["result"]
    return ResourceTuple(
        id=resource_id,
        name=result["name"],
        when_created=datetime.fromisoformat(result["created"]).replace(tzinfo=tz),
        mimetype=result["mimetype"],
        url=result["url"],
        package_id=result["package_id"],
    )


# Get the file's content
def get_resource_content(resource):
    res = requests.get(resource.url)
    res.raise_for_status()
    return res.content


# get package id from resource, and then package name from package
def get_package_name(resource, website):
    package_show = f"{website}/api/3/action/package_show"
    res = requests.get(package_show, params={"id": resource.package_id})
    res.raise_for_status()
    j = res.json()
    return j["result"]["title"]


def process_resource_impl(resource, website, force):
    logger.info(f"processing resource {resource}")
    try:
        content = get_resource_content(resource)
        calendar_name = get_package_name(resource, website=website)
        process_calendar(
            resource_id=resource.id,
            calendar_name=calendar_name,
            when_created_at_source=resource.when_created,
            file_stream=content,
            force=force,
        )
    except Exception as e:
        status = "Exception"
        detail = traceback.format_exc()
        logger.exception(f"resource {resource}")
    else:
        status = "Success"
        detail = None

    DownloadReport(resource_id=resource.id, status=status, detail=detail).save()


def process_resource(resource_id, website, force):
    resource = get_resource(
        resource_id=resource_id,
        website=website,
    )
    process_resource_impl(resource, website, force)
