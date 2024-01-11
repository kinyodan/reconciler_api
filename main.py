from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from helpers.application_helpers import *
from helpers.csv_helpers import *
from helpers.validation_helpers import *
from helpers.status_helper import *
from helpers.recon_helper import *
import json
import random


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# load error_messeges json file
error_messeges_file = open("error_messeges.json")
error_messeges_set = json.load(error_messeges_file)
error_messeges = error_messeges_set["messeges"]


@app.get("/")
async def root():
    return {"status": True, "messege": "Hello from Credrails Api you are Home"}


# Path to post data for upload
@app.post("/upload_data_files")
async def upload_data_files(source: UploadFile, target: UploadFile):
    status = True
    upload_file_tag_id = random.randint(1000, 10000)
    validate_upload_files(source, "Source file")
    validate_upload_files(target, "Target file")
    status = csv_helper_write_upload_files(
        source.file.read(), target.file.read(), upload_file_tag_id
    )
    status_helper_verify_status(status, 422, error_messeges["write_upload"])

    data = recon_helpers_process_uploads_for_recon(upload_file_tag_id)

    return {
        "status": status,
        "messege": "files upload done",
        "write_folder_number": upload_file_tag_id,
        "data": data,
    }


# Api call yo generate large size csv files to upload for testing if app can scale
# dafault is set to 10000 records for each file
@app.get("/genarate_test_csv_files")
async def generate_test_csv_files(filename: str, number_of_records: int):
    result = csv_helpers_write_very_large_File(filename, number_of_records)

    return {
        "status": result,
        "messege": "test files written for you , find them in the apps root folder inside /test_csv_files folder ,you can use them as upload files",
    }
