import os
from requests import Response


XRAY_VARS = {
    "XRAY_API_BASE_URL": "http://127.0.0.1:5002",
    "XRAY_API_USER": "jirauser",
    "XRAY_API_PASSWORD": "jirapassword",
    "XRAY_CLIENT_ID": "client_id",
    "XRAY_CLIENT_SECRET": "client_secret"
}


def mocked_xray_server_request(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

        def raise_for_status(self):
            req = Response()
            req.status_code = self.status_code
            return req.raise_for_status()

    method = args[0] if len(args) > 0 else kwargs.get("method") or ""
    url = args[1] if len(args) > 1 else kwargs.get("url") or ""

    base_url = os.environ['XRAY_API_BASE_URL']
    if method.lower() == "post":
        if url == f"{base_url}/rest/raven/2.0/import/execution":
            return MockResponse({'testExecIssue': {'key': '1000'}}, 200)
        elif url == f"{base_url}/api/v2/import/execution":
            return MockResponse({'key': '1000'}, 200)
        elif url == f"{base_url}/api/v2/authenticate":
            return MockResponse({'status': 'OK'}, 200)

    return MockResponse(None, 404)
