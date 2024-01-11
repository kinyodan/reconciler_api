from fastapi import HTTPException


def status_helper_verify_status(status, status_code_incase_false, messege):
    if status is False:
        raise HTTPException(status_code=status_code_incase_false, detail=messege)
