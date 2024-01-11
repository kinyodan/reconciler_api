from http import HTTPStatus
from pathlib import PurePath
from fastapi import Path
from fastapi.testclient import TestClient
import os
from os.path import exists
from main import app
import csv
import json


credrails_client = TestClient(app)


def test_main_read():
    response = credrails_client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "status": True,
        "messege": "Hello from Credrails Api you are Home",
    }


def test_upload_data_files_without_any_file_input():
    response = credrails_client.post("/upload_data_files")
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "source"],
                "msg": "field required",
                "type": "value_error.missing",
            },
            {
                "loc": ["body", "target"],
                "msg": "field required",
                "type": "value_error.missing",
            },
        ]
    }

# Testing when one file is absent 
def test_upload_data_files_without_only_source_file_input():
    test_source_upload_file = "test_csv_files/source-test.csv"

    with open(test_source_upload_file, "rb") as source:
            response = credrails_client.post(
                "/upload_data_files",
                files={"source": ("source", source, "text/csv"), "target": ""})
            assert response.status_code == 415
            assert response.json() == {
                "detail": "Unsupported file type => Target file"
                }


def test_upload_data_files_without_only_target_file_input():
    test_target_upload_file = "test_csv_files/target-test.csv"

    with open(test_target_upload_file, "rb") as target:
            response = credrails_client.post(
                "/upload_data_files",
                files={"target": ("target", target, "text/csv"), "source": ""})
            assert response.status_code == 415
            assert response.json() == {
                "detail": "Unsupported file type => Source file"
                }


# testing full upload whne all is present 
def test_upload_data_files_with_file_input():
    test_source_upload_file = "test_csv_files/source-test.csv"
    test_target_upload_file = "test_csv_files/target-test.csv"

    with open(test_source_upload_file, "rb") as source:
        with open(test_target_upload_file, "rb") as target:
            response = credrails_client.post(
                "/upload_data_files",
                files={"source": ("source", source, "text/csv"), "target": ("target",target, "text/csv")})
            assert response.status_code == 200
            assert response.json()["status"] == True
            assert response.json()["messege"] == "files upload done"
            assert response.json()["write_folder_number"] != None


