from fastapi import HTTPException, status
from typing import IO


def validate_upload_files(file: IO, field: str):
    accepted_file_types = ["text/csv"]

    if file.content_type not in accepted_file_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type => {field}",
        )
