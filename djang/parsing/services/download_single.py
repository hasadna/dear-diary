from typing import NamedTuple
import requests
import traceback

from .parser import process_calendar
from ..models import DownloadReport

class ResourceTuple(NamedTuple):
    id: str
    name: str
    mimetype: str
    url: str
    package_id: str

def get_resource(resource_id: str, website:str):
    resource_show = f"{website}/api/3/action/resource_show"
    res = requests.get(resource_show, params={"id":resource_id})
    res.raise_for_status()
    j = res.json()
    result = j['result']
    return ResourceTuple(
        id=resource_id,
        name=result['name'],
        mimetype=result['mimetype'],
        url=result['url'],
        package_id=result['package_id'],
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
    return j['result']['title']

def process_resource_impl(resource, website, force):
    content = get_resource_content(resource)
    calendar_name = get_package_name(resource, website=website)
    process_calendar(
        resource_id=resource.id,
        calendar_name=calendar_name,
        file_stream=content,
        force=force,
    )

def process_resource(resource_id, website, force):
    try:
        resource = get_resource(
            resource_id=resource_id,
            website=website,
        )
        process_resource_impl(resource, website, force)
    except Exception as e:
        status = "Exception"
        detail = traceback.format_exc()
    else:
        status = "Success"
        detail = None

    DownloadReport(
        resource_id=resource_id,
        status=status,
        detail=detail
    ).save()


