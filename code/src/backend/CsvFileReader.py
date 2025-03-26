import csv


def load_request_types(csv_file):
    request_types = {}  # Dictionary to store request types and sub-request types

    with open(csv_file, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row if it exists

        for row in reader:
            request_type = row[0].strip()
            sub_request_type = row[1].strip() if len(row) > 1 else None

            if request_type in request_types:
                if sub_request_type and sub_request_type != "-":
                    request_types[request_type].append(sub_request_type)
            else:
                request_types[request_type] = [sub_request_type] if sub_request_type and sub_request_type != "-" else []

    return request_types