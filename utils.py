import os
import logging
import uuid

UPLOAD_DIR = "file_uploaded"


def create_upload_dir_if_not_exist():
    try:
        os.mkdir(UPLOAD_DIR)
    except Exception as e:
        logging.error("Error creating upload directory: {}".format(e.__str__()))


def generate_file_id(filename):
    # this will return a tuple of root and extension
    split_tup = os.path.splitext(filename)
    new_file_id = "{}.{}".format(uuid.uuid4(),split_tup[1].replace(".",""))

    return new_file_id