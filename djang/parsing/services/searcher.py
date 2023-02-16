import requests

from .download import ResourceTuple, process_resource_impl

from ..models import Calendar

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
            mimetype=result['mimetype'],
            url=result['url'],
            package_id=result['package_id'],
        )

def filter_resource(resource) -> bool:
    if resource.mimetype != "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        return False

    if Calendar.objects.filter(resource_id=resource.id).exists():
        return False

    return True

def process_resources(query: str, website: str, force: bool):
    # TODO this should be a separate task when we fully implement this
    resources = get_resources(query, website)
    resources = [
        r for r in resources
        if filter_resource(r)
    ]
    for resource in resources:
        process_resource_impl(resource, website, force)
