from datetime import datetime, timezone

from fastapi import FastAPI, Response
from fastapi.responses import (
    FileResponse,
    JSONResponse,
    RedirectResponse,
)
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()


### Default JSON Response
@app.get(
    "/time",
    response_class=JSONResponse,
)
def get_current_time():
    return {
        "timestamp": datetime.now(),
    }


### File Response
@app.get(
    "/file",
    response_class=FileResponse,
)
def get_file():
    return "path/to/file"  # as Path


### Redirect Response
@app.get(
    "/timenow",
    response_class=RedirectResponse,
)
def get_time_now():
    # Redirect URL
    return "/utcnow"


@app.get("/utcnow")
def get_utc_time():
    return {
        "timestamp": datetime.now(timezone.utc),
    }


### Custom Response Class
class UpperResponse(Response):
    # Initialize the default response attributes
    def __init__(
        self,
        content=None,
        status_code=200,
        headers=None,
        media_type=None,
        background=None,
    ):
        super().__init__(content, status_code, headers, media_type, background)

    # Render the response and make changes to the content as needed
    def render(self, content):
        content = content.upper()
        return super().render(content)


@app.get(
    "/custom",
    response_class=UpperResponse,
)
def get_custom_response():
    return "be bold!"


### Scalar API Documentation
@app.get("/scalar", include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title="Scalar API",
    )
