from flask import Blueprint, flash, request, Response, send_file, after_this_request
import json
import os
from datetime import datetime
import uuid
from configs import config
from . import gcs, db, logger

files_api_v1 = Blueprint('files_api_v1', __name__, url_prefix='/api/v1/files')

config = config.get_config()

# Set up the logger
logger = logger.setup_logger(config["LOGS_FOLDER"])

# Initialize the GCSHandler with the path to service account credentials file
gcs_handler = gcs.GCSHandler(config['gcs']['credentials_json'], logger)

# Initialize the FileMetadataDB with Mongo URI and database name
file_metadata_db = db.FileMetadataDB(config['mongo']['uri'], config['mongo']['db_name'], logger)


def save_file_to_tmp_dir(f):
    tmp_dir = config['tmp_dir']

    # Create the directory if it does not exist
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    file_path = os.path.join(tmp_dir, f.filename)
    f.save(file_path)
    logger.info(f"Saved file at {file_path}")

    return file_path


def create_file_metadata(f, tmp_file_path, file_name: str):
    file_id = str(uuid.uuid4())
    size_in_bytes = os.path.getsize(tmp_file_path)
    file_type = f.mimetype
    created_at = datetime.utcnow().isoformat()
    updated_at = datetime.utcnow().isoformat()
    blob_name = file_id

    # ext is the file extension including the dot ('.')
    _, ext = os.path.splitext(f.filename)

    file_metadata = {
        "_id": file_id,
        "file_name": file_name,
        "size_in_bytes": size_in_bytes,
        "file_type": file_type,
        "file_ext": ext.strip("."),
        "created_at": created_at,
        "updated_at": updated_at,
        "blob_name": blob_name
    }
    return file_metadata


@files_api_v1.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Check if the 'file' key is in the request.files dict
        if 'file' not in request.files or not request.files['file']:
            logger.error(f'Failed to upload file as file is not selected')
            response = {"status": False, "error": "No file selected", "message": "Failed to upload file"}
            return Response(response=json.dumps(response), status=400, mimetype="application/json")

        # Check if 'file_name' is provided
        file_name = request.form.get('file_name')
        if not file_name:
            logger.error(f'Failed to upload file as file_name is not provided')
            response = {"status": False, "error": "Missing file_name", "message": "Failed to upload file"}
            return Response(response=json.dumps(response), status=400, mimetype="application/json")

        f = request.files['file']
        tmp_file_path = save_file_to_tmp_dir(f)
        file_metadata = create_file_metadata(f, tmp_file_path, file_name)

        gcs_handler.upload_blob(config['gcs']['bucket_name'], tmp_file_path, file_metadata["blob_name"])

        file_metadata_db.insert(file_metadata)

        response = {"status": True, "error": "", "message": "Successfully uploaded the file", "data": file_metadata}
        return Response(response=json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {"status": False, "error": str(e), "message": f"Failed to upload file"}
        return Response(response=json.dumps(response), status=500, mimetype="application/json")


@files_api_v1.route('/<file_id>', methods=['GET'])
def read_file(file_id):
    try:
        file_metadata = file_metadata_db.get(file_id)
        if file_metadata:
            desired_filename = f"{file_metadata['file_name']}.{file_metadata['file_ext']}"
            # tmp_dir = config['tmp_dir']
            # download_file_path = os.path.join(
            #     os.getcwd(),
            #     tmp_dir,
            #     desired_filename
            # )
            #
            # gcs_handler.download_blob(config['gcs']['bucket_name'], file_metadata["blob_name"], download_file_path)
            #
            # # Send file data as a response #
            # return send_file(download_file_path, as_attachment=True)

            signed_url = gcs_handler.generate_download_signed_url(config['gcs']['bucket_name'],
                                                                  file_metadata["blob_name"], desired_filename)
            response = {"status": True, "error": "", "message": "Successfully uploaded the file",
                        "data": {"signed_url": signed_url, "metadata": file_metadata}}
            return Response(response=json.dumps(response), status=200, mimetype="application/json")
        else:
            response = {"status": False, "error": "File not found", "message": f"Failed to read file {file_id}"}
            return Response(response=json.dumps(response), status=404, mimetype="application/json")

    except Exception as e:
        response = {"status": False, "error": str(e), "message": f"Failed to read file {file_id}"}
        return Response(response=json.dumps(response), status=500, mimetype="application/json")


@files_api_v1.route('/<file_id>', methods=['DELETE'])
def delete_file(file_id):
    try:
        file_metadata = file_metadata_db.get(file_id)
        if file_metadata:
            gcs_handler.delete_blob(config['gcs']['bucket_name'], file_metadata["blob_name"])
            file_metadata_db.delete(file_id)
            response = {"status": True, "error": "", "message": f"Successfully deleted the File {file_id}"}
            return Response(response=json.dumps(response), status=200, mimetype="application/json")
        else:
            response = {"status": False, "error": "File not found", "message": f"Failed to delete file {file_id}"}
            return Response(response=json.dumps(response), status=404, mimetype="application/json")
    except Exception as e:
        response = {"status": False, "error": str(e), "message": f"Failed to delete file {file_id}"}
        return Response(response=json.dumps(response), status=500, mimetype="application/json")


@files_api_v1.route('/<file_id>', methods=['PUT'])
def update_file(file_id):
    try:
        existing_metadata = file_metadata_db.get(file_id)
        if existing_metadata:
            new_file_metadata = existing_metadata.copy()

            if 'file' in request.files and request.files['file']:
                f = request.files['file']
                tmp_file_path = save_file_to_tmp_dir(f)
                new_file_metadata.update({
                    "size_in_bytes": os.path.getsize(tmp_file_path),
                    "file_type": f.mimetype,
                    "updated_at": datetime.utcnow().isoformat(),
                    "file_ext": os.path.splitext(f.filename)[1].strip(".")
                })
                gcs_handler.upload_blob(config['gcs']['bucket_name'], tmp_file_path, existing_metadata["blob_name"])

            new_file_name = request.form.get('file_name')
            if new_file_name:
                new_file_metadata.update({
                    "file_name": new_file_name,
                    "updated_at": datetime.utcnow().isoformat(),
                })

            file_metadata_db.update(new_file_metadata)

            response = {"status": True, "error": "", "message": f"Successfully updated file {file_id}"}
            return Response(response=json.dumps(response), status=200, mimetype="application/json")

    except Exception as e:
        response = {"status": False, "error": str(e), "message": f"Failed to update file {file_id}"}
        return Response(response=json.dumps(response), status=500, mimetype="application/json")


@files_api_v1.route('/', methods=['GET'])
def list_files():
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', config["DEFAULT_FILES_PER_PAGE"], type=int)
        search_term = request.args.get('q')

        files = file_metadata_db.get_paginated(page, limit, search_term)

        response = {"status": True, "error": "", "data": files}
        return Response(response=json.dumps(response), status=200, mimetype="application/json")
    except Exception as e:
        response = {"status": False, "error": str(e), "data": []}
        return Response(response=json.dumps(response), status=500, mimetype="application/json")
