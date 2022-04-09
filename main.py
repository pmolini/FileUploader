from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse
import shutil
from starlette.requests import Request
from utils import UPLOAD_DIR, create_upload_dir_if_not_exist, generate_file_id
from starlette.responses import FileResponse

app = FastAPI()


# Endpoint for file uploading
# it can accept a list of file as input
# the files will be stored in a defined directory and a url for download the file will be gererated
@app.post("/uploadfiles/")
async def create_upload_files(request: Request,
                              files: List[UploadFile] = File(..., description="Multiple files as UploadFile")):
    resp = []
    for file in files:
        # Create the directory if doesn't exist
        create_upload_dir_if_not_exist()
        # generate a file id
        new_name = generate_file_id(file.filename)
        # save the file to disk
        with open("{}/{}".format(UPLOAD_DIR, new_name), "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        resp.append({"original_name": file.filename,
                     "link": "{}{}{}".format(request.base_url, "download_file/?file_id=", new_name)})
    return {"upload results": resp}


# endpoint for download file
# it need the file_id as a query parameter
@app.get("/download_file/")
async def file_download(file_id):
    print("{}/{}".format(UPLOAD_DIR, file_id))
    return FileResponse("{}/{}".format(UPLOAD_DIR, file_id), media_type='application/octet-stream', filename=file_id)
    # return FileResponse(UPLOAD_DIR, media_type='application/octet-stream', filename=file_id)


# Serve a static HTML for test the application
@app.get("/")
async def main():
    content = """
<body>
</h1> EVA test - File uploade </h1>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
