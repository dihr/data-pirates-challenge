import json


class DataWriter:
    def __init__(self, file_extension):
        self.file_extension = file_extension

    def write_location_data(self, file_name, data):
        output_filepath = f"{file_name}.{self.file_extension}"
        with open(output_filepath, "w") as jsonl_file:
            json.dump(data, jsonl_file, indent=4, ensure_ascii=False)