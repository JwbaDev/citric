# How-to Guide

For the full JSON-RPC reference, see the [RemoteControl 2 API docs][rc2api].

## Get surveys and questions

```python
from citric import Client

LS_URL = "http://localhost:8001/index.php/admin/remotecontrol"

with Client(LS_URL, "iamadmin", "secret") as client:
    # Get all surveys from user "iamadmin"
    surveys = client.list_surveys("iamadmin")

    for s in surveys:
        print(s["surveyls_title"])

        # Get all questions, regardless of group
        questions = client.list_questions(s["sid"])
        for q in questions:
            print(q["title"], q["question"])
```

## Export responses to a `pandas` dataframe

```python
import io
import pandas as pd

survey_id = 123456

df = pd.read_csv(
    io.BytesIO(client.export_responses(survey_id, file_format="csv")),
    delimiter=";",
    parse_dates=["datestamp", "startdate", "submitdate"],
    index_col="id",
)
```

## Use custom `requests` session

It's possible to use a custom session object to make requests. For example, to cache the requests
and reduce the load on your server in read-intensive applications, you can use
[`requests-cache`](https://requests-cache.readthedocs.io):

```python
import requests_cache

cached_session = requests_cache.CachedSession(
    expire_after=3600,
    allowable_methods=["POST"],
)

with Client(
    LS_URL,
    "iamadmin",
    "secret",
    requests_session=cached_session,
) as client:

    # Get all surveys from user "iamadmin"
    surveys = client.list_surveys("iamadmin")

    # This should hit the cache. Running the method in a new client context will
    # not hit the cache because the RPC session key would be different.
    surveys = client.list_surveys("iamadmin")
```

## Use a different authentication plugin

By default, this client uses the internal database for authentication but
{ls_manual}`arbitrary plugins <Authentication_plugins>` are supported by the
`auth_plugin` argument.

```python
with Client(
    LS_URL,
    "iamadmin",
    "secret",
    auth_plugin="AuthLDAP",
) as client:
    ...
```

Common plugins are `Authdb` (default), `AuthLDAP` and `Authwebserver`.

## Get files uploaded to a survey and move them to S3

```python
import boto3
from citric import Client

s3 = boto3.client("s3")

with Client(
    "https://mylimeserver.com/index.php/admin/remotecontrol",
    "iamadmin",
    "secret",
) as client:
    survey_id = 12345
    for file in client.get_uploaded_file_objects(survey_id):
        s3.upload_fileobj(
            file.content,
            "my-s3-bucket",
            f"uploads/sid={survey_id}/qid={file.meta.question.qid}/{file.meta.filename}",
        )
```

## Use the raw `Client.session` for low-level interaction

This library doesn't (yet) implement all RPC methods, so if you're in dire need of using a method not currently supported, you can use the `session` attribute to invoke the underlying RPC interface without having to pass a session key explicitly:

```python
# Call the copy_survey method, not available in Client
with Client(LS_URL, "iamadmin", "secret") as client:
    new_survey_id = client.session.copy_survey(35239, "copied_survey")
```

## Notebook samples

- [Import a survey file from S3](https://github.com/edgarrmondragon/citric/blob/main/docs/notebooks/import_s3.ipynb)
- [Download responses and save them to a SQLite database](https://github.com/edgarrmondragon/citric/blob/main/docs/notebooks/pandas_sqlite.ipynb)

[rc2api]: https://api.limesurvey.org/classes/remotecontrol_handle.html