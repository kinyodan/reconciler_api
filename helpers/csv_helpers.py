import csv
import os
from os.path import exists
import random
from faker import Faker

fake = Faker()


def csv_helper_write_upload_files(source, target, file_tag_id):
    status = False
    check_or_create_directory(f"uploads/{file_tag_id}")
    status = write_to_file(source, f"uploads/{file_tag_id}/{file_tag_id}-source.csv")
    status = write_to_file(target, f"uploads/{file_tag_id}/{file_tag_id}-target.csv")
    return status


def csv_helpers_write_reports_to_csv(
    unique_to_source, unique_to_target, discrepant, folder_id
):
    check_or_create_directory(f"reports/{folder_id}")

    write_unique_to_source_csv(folder_id,unique_to_source)
    write_unique_to_target_csv(folder_id,unique_to_target)
    write_descrepant_csv_report(folder_id,discrepant)


def write_unique_to_source_csv(folder_id, unique_to_source):
    with open(f"reports/{folder_id}/unique_to_source.csv", "w", newline="") as csvfile:
        fieldnames = ["ID", "Name", "Date", "Amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in unique_to_source:
            writer.writerow(
                {
                    "ID": i["ID"],
                    "Name": i["Name"],
                    "Date": i["Date"],
                    "Amount": i["Amount"],
                }
            )


def write_unique_to_target_csv(folder_id,unique_to_target):
    with open(f"reports/{folder_id}/unique_to_target.csv", "w", newline="") as csvfile:
        fieldnames = ["ID", "Name", "Date", "Amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in unique_to_target:
            writer.writerow(
                {
                    "ID": i["ID"],
                    "Name": i["Name"],
                    "Date": i["Date"],
                    "Amount": i["Amount"],
                }
            )


def write_descrepant_csv_report(folder_id,discrepant):
    with open(f"reports/{folder_id}/discrepant.csv", "w", newline="") as csvfile:
        fieldnames = [ "ID" ,"feild_name", "source_data_value", "target_data_value"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for i in discrepant:
            record = discrepant[f"{i}"]
            writer.writerow(
                {
                    "ID": f"{i}",
                    "feild_name": record["feild_name"],
                    "source_data_value": record["source_data_value"],
                    "target_data_value": record["target_data_value"],
                }
            )


def write_to_file(file, path):
    with open(path, "wb+") as file_object:
        file_object.write(file)

    if exists(path):
        return True
    else:
        return False


def check_or_create_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


# THIS METHOD IS NOT INTEGRAL TO THE OPERATIONS OF THE APP IT IS FOR TESTING PUPOSES
# TO ALLOW  YOU THE USER TO GENERATE LARGE CSV FILES WITH THE RELEVANT FIELDS ON THE FLY
# HENCE THE UNOTHORDOX WAY IT HAS BEEN  WRITTEN AS ITS RATHER LARGE IN SIZE COMPARED TO OTHER METHODS AND LESS FORMATTED
def csv_helpers_write_very_large_File(filename, number_of_records=10000):
    names = []
    # write data to our csv file
    with open(f"test_csv_files/source-{filename}.csv", "w", newline="") as csvfile:
        fieldnames = ["ID", "Name", "Date", "Amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        increment = 0
        for i in range(number_of_records):
            names.append(fake.name())
            writer.writerow(
                {
                    "ID": "%08g" % (int("000000001") + increment),
                    "Name": names[i],
                    "Date": "2023-01-02",
                    "Amount": random.randint(100, 500),
                }
            )
            increment = increment + 1

        for i in range(1000):
            names.append(fake.name())
            writer.writerow(
                {
                    "ID": "%08g" % (int("000000001") + increment),
                    "Name": fake.name(),
                    "Date": "2023-01-02",
                    "Amount": random.randint(100, 500),
                }
            )
            increment = increment + random.randint(100, 5000)

    # write data to our csv file
    with open(f"test_csv_files/target-{filename}.csv", "w", newline="") as csvfile:
        fieldnames = ["ID", "Name", "Date", "Amount"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        increment = 0
        for i in range(number_of_records):
            writer.writerow(
                {
                    "ID": "%08g" % (int("000000001") + increment),
                    "Name": names[i],
                    "Date": "2023-01-02",
                    "Amount": random.randint(100, 500),
                }
            )
            increment = increment + 1

        for i in range(1000):
            names.append(fake.name())
            writer.writerow(
                {
                    "ID": "%08g" % (int("000000001") + increment),
                    "Name": fake.name(),
                    "Date": "2023-01-02",
                    "Amount": random.randint(100, 500),
                }
            )
            increment = increment + random.randint(100, 5000)

    return True
