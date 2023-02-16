from typing import NamedTuple
import requests

from .parser import process_calendar

class ResourceTuple(NamedTuple):
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

def process_resource(resource_id, website, force):
    resource = get_resource(
        resource_id=resource_id,
        website=website,
    )
    content = get_resource_content(resource)
    calendar_name = get_package_name(resource, website=website)
    process_calendar(
        resource_id=resource_id,
        calendar_name=calendar_name,
        file_stream=content,
        force=force,
    )
