
## API Documentation

1. **Upload File API**
    
   Uploads a file to the cloud storage, returning file metadata as a response.
    
   **Endpoint:** ```POST /api/v1/files/upload```

   **Request:**
   ```bash
   curl --location --request POST 'http://localhost:5000/api/v1/files/upload' \
   --form 'file=@"/test/sample_file.jpg"' \
   --form 'file_name="Test File Upload"'
   ```

   **Response:**
   ```json
   {
       "status": true,
       "error": "",
       "message": "Successfully uploaded the file",
       "data": {
           "_id": "2731db21-a999-4958-ae6b-498660b7656a",
           "file_name": "Test File Upload",
           "size_in_bytes": 7470307,
           "file_type": "image/jpeg",
           "file_ext": "jpg",
           "created_at": "2024-01-10T12:55:27.746036",
           "updated_at": "2024-01-10T12:55:27.746045",
           "blob_name": "2731db21-a999-4958-ae6b-498660b7656a"
       }
   }
   ```
2.  **List All Files API**

    Responds with metadata of all files. It supports pagination and case-insensitive search on file name.
    
    **Endpoint:** ```GET /api/v1/files```
    
    **Request:**
    ```bash
    curl --location --request GET 'http://localhost:5000/api/v1/files?page=1&limit=10&q=sample'
    ```
    
    **Response:**
    ```json
    {
    "status": true,
    "error": "",
    "data": [
        {
            "_id": "2731db21-a999-4958-ae6b-498660b7656a",
            "file_name": "Test File Upload",
            "size_in_bytes": 7470307,
            "file_type": "image/jpeg",
            "file_ext": "JPG",
            "created_at": "2024-01-10T12:55:27.746036",
            "updated_at": "2024-01-10T12:55:27.746045",
            "blob_name": "2731db21-a999-4958-ae6b-498660b7656a"
        },
        // ... Additional file metadata entries ...
      ]
    }
    ```
3. **Download/Read File API**
    
   Downloads a file by providing the unique file identifier, returning a signed URL for file download.
    
   **Endpoint:** ```GET /api/v1/files/{file_id}```

   **Request:**
   ```bash
   curl --location --request GET 'http://localhost:5000/api/v1/files/2731db21-a999-4958-ae6b-498660b7656a'
   ```

   **Response:**
   ```json
   {
    "status": true,
    "error": "",
    "message": "Successfully uploaded the file",
    "data": {
        "signed_url": "// Signed URL //" ,
        "metadata": {
            "_id": "2731db21-a999-4958-ae6b-498660b7656a",
            "file_name": "Test File Upload",
            "size_in_bytes": 7470307,
            "file_type": "image/jpeg",
            "file_ext": "JPG",
            "created_at": "2024-01-10T12:55:27.746036",
            "updated_at": "2024-01-10T12:55:27.746045",
            "blob_name": "2731db21-a999-4958-ae6b-498660b7656a"
        }
      }
    }
   ```
4. **Delete File API**
    
   Deletes a file by providing the unique file identifier, deleting both file metadata and the actual file.
    
   **Endpoint:** ```DELETE /api/v1/files/{file_id}```

   **Request:**
   ```bash
   curl --location --request DELETE 'http://localhost:5000/api/v1/files/2731db21-a999-4958-ae6b-498660b7656a'
   ```

   **Response:**
   ```json
   {
    "status": true,
    "error": "",
    "message": "Successfully deleted the File 2731db21-a999-4958-ae6b-498660b7656a"
    }
   ```
5. **Update File API**
    
    Update an existing file or its filename
    
    **Endpoint**: ```PUT /api/v1/files/{file_id}```

    **Request:**
    ```bash
    curl --location --request PUT 'http://localhost:5000/api/v1/files/a33276ea-09af-4432-b737-9726a7342632' \
    --form 'file_name="Updated Name"' \
    --form 'file=@"/test/sample_file_2.jpg"'
    ```
    
    **Response:**
    ```json
    {
      "status": true,
      "error": "",
      "message": "Successfully updated file 1d35e6f2-59bf-4e36-9336-3843b67e41b8"
    }
   ```
    