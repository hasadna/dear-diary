import requests

from parsing import models

RESOURCE_SHOW = "https://www.odata.org.il/api/3/action/resource_show"
ACCEPTABLE_MIMETYPES = {
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

}

def import_single(resource_id: str, force: bool) -> None:
    # Ensure not created already, or --force
    file_exists = models.FileImportResult.objects.filter(resource_id=resource_id).exists()
    if file_exists and not force:
        # TODO logger
        print("already exists")
        return
    try:
        # Get record
        resp = requests.get(RESOURCE_SHOW, params={"id":resource_id})
        resp.raise_for_status()
        info = resp.json() 
        assert info['success']
        info = info['result']
        # Ensure mimetype works
        mime_type = info['mimetype']
        assert mime_type in ACCEPTABLE_MIMETYPES
        # Get actual file
        models.UnprocessedFile(
            resource_id=resource_id,
            mime_type=mime_type,
            name=info['name'],
            url=info['url'],
        ).save()
        e = None
    except Exception as exc:
        e = exc

    models.FileImportResult(
        resource_id=resource_id,
        result_is_successful=(e is None),
        result_error=str(e) if e else None,
    ).save()
