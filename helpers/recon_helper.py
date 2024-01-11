from fastapi import HTTPException
from os.path import exists
import threading
import csv
from helpers.csv_helpers import *


def recon_helpers_process_uploads_for_recon(upload_file_tag_id, filter_fields=False):
    check_data_file_exists(upload_file_tag_id, "source.csv")
    check_data_file_exists(upload_file_tag_id, "target.csv")

    for_feild_comparison = {}
    source_data = read_data_file(upload_file_tag_id, "source.csv")

    target_data = read_data_file(upload_file_tag_id, "target.csv")

    dict_source_data = convert_to_data_hash(source_data)
    dict_taget_data = convert_to_data_hash(target_data)

    checked_for_source_file = try_get_present_in_one_missing_in_other(
        source_data, dict_taget_data["data"]
    )
    present_in_both = checked_for_source_file["present_keys"]
    for_feild_comparison["source_data"] = present_in_both

    checked_for_target_file = try_get_present_in_one_missing_in_other(
        target_data, dict_source_data["data"]
    )
    present_in_both = checked_for_target_file["present_keys"]
    for_feild_comparison["target_data"] = present_in_both

    discrepant_feilds = compare_each_field_for_present_in_both(for_feild_comparison)

    csv_helpers_write_reports_to_csv(
        checked_for_source_file["missing_keys"],
        checked_for_target_file["missing_keys"],
        discrepant_feilds,
        upload_file_tag_id,
    )

    return {
        "unique_to_source_file": checked_for_source_file["missing_keys"],
        "unique_to_target_file": checked_for_target_file["missing_keys"],
        "discrepant_feilds": discrepant_feilds,
    }


def check_data_file_exists(upload_file_tag_id, file_name):
    if not exists(f"uploads/{upload_file_tag_id}/{upload_file_tag_id}-{file_name}"):
        raise HTTPException(
            status_code=422,
            detail=f"problem processing uploads for recon {file_name} file mising",
        )


def read_data_file(upload_file_tag_id, file_name):
    return [
        *csv.DictReader(
            open(f"uploads/{upload_file_tag_id}/{upload_file_tag_id}-{file_name}")
        )
    ]


def convert_to_data_hash(data, discrepant_data=[]):
    data_hash = {}
    for key in data:
        if "ID" in key:
            data_hash[f"{key['ID']}"] = key
        else:
            discrepant_data.append(key)

    return {"data": data_hash, "discrepant_data": discrepant_data}


def try_get_present_in_one_missing_in_other(main_data, other_data):
    present_keys = {}
    missing_keys = []
    for k in main_data:
        if f"{k['ID']}" in other_data:
            present_keys[f"{k['ID']}"] = k
        else:
            missing_keys.append(k)

    return {"missing_keys": missing_keys, "present_keys": present_keys}


def compare_each_field_for_present_in_both(comparison_data):
    discrepant_feilds = {}
    for key in comparison_data["source_data"]:
        source_data_key = comparison_data["source_data"][f"{key}"]
        target_data_key = comparison_data["target_data"][f"{key}"]
        result = [
            (k, source_data_key[k], target_data_key[k])
            for k in source_data_key
            if k in target_data_key and source_data_key[k] != target_data_key[k]
        ]

        if len(result) > 0:
            discrepant_feilds[f"{key}"] = {
                "feild_name": result[0][0],
                "source_data_value": result[0][1],
                "target_data_value": result[0][2],
            }

    return discrepant_feilds


def field_compare(field, field_other):
    if field == field_other:
        return True
    else:
        return False
