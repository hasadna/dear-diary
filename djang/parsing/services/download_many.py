import requests
from datetime import datetime

from .download_single import ResourceTuple, process_resource_impl
from ..models import Calendar, DownloadReport

from django_q.tasks import async_task

class defaults:
    website = "https://www.odata.org.il"
    query = "name:יומן"

def get_resources(query: str, website: str):
    resource_search = f"{website}/api/3/action/resource_search"
    res = requests.get(resource_search, params={"query":query})
    res.raise_for_status()
    j = res.json()
    results = j['result']['results']
    for result in results:
        yield ResourceTuple(
            id=result['id'],
            name=result['name'],
            # TODO make this timezone aware
            when_created=datetime.fromisoformat(result['created']),
            mimetype=result['mimetype'],
            url=result['url'],
            package_id=result['package_id'],
        )

def filter_resource(resource, force:bool) -> bool:
    if resource.mimetype != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return False

    if not force and Calendar.objects.filter(resource_id=resource.id).exists():
        return False

    return True

def process_resources(query: str, website: str, force: bool, use_q:bool):
    # TODO this should be a separate task when we fully implement this
    resources = get_resources(query, website)

    # Classic loop rather than list composition so we can implement an "else" logging "skipped"
    filtered_resources = []
    for resource in resources:
        if filter_resource(resource, force=force):
            filtered_resources.append(resource)

    for resource in filtered_resources:
        try:
            if use_q:
                async_task(process_resource_impl, resource, website, force)
            else:
                process_resource_impl(resource, website, force)
        except Exception as e:
            print(e)


def process_resources_default():
    return process_resources(
        query=defaults.query,
        website=defaults.website,
        force=False,
        use_q=True,
    )
