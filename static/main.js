const HOST = "10.103.116.51"
const PORT = "5000"
const BASE_URL = `http://${HOST}:${PORT}/api/v1/files`;
const UPLOAD_FILE_API = `${BASE_URL}/upload`

toastr.options = {
    "closeButton": true,
    "debug": false,
    "newestOnTop": false,
    "progressBar": false,
    "positionClass": "toast-top-right",
    "preventDuplicates": false,
    "onclick": null,
    "showDuration": "30",
    "hideDuration": "1000",
    "timeOut": "3000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
  }

document.addEventListener('DOMContentLoaded', function () {
    fetchFiles();
});

function uploadFile() {
    const fileInput = document.getElementById('file');
    const fileNameInput = document.getElementById('fileName');

    // Check if file is selected
    if (!fileInput.files[0]) {
        toastr.error('Please choose a file before uploading');
        return;
    }

    // Check if file name is given
    if (!fileNameInput.value.trim()) {
        toastr.error('Please enter a file name before uploading');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('file_name', fileNameInput.value);
    toastr.success('Uploading the file. Page will reload on successful upload')
    fetch(UPLOAD_FILE_API, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if(data.status) {
            console.log('File uploaded successfully with fileId:', data.fileId);
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        toastr.success('Error uploading file')
    });
}

function fetchFiles() {
    fetch(`${BASE_URL}`)
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                populateFileList(data.data);
            } else {
                console.error('Error fetching files:', data.error);
                //TODO: Implement handling the error and updating the UI accordingly
            }
        })
        .catch(error => {
            console.error('Error fetching files:', error);
            //TODO: Implement handling the error and updating the UI accordingly
        });
}

function downloadFile(fileId) {
    fetch(`${BASE_URL}/${fileId}`, {
        method: "GET"
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            const signedUrl = data.data.signed_url;
            initiateFileDownload(signedUrl);
        } else {
            console.error('Error fetching signed URL:', data.error);
            // Handle the error and update the UI accordingly
        }
    })
    .catch(error => {
        console.error('Error fetching signed URL:', error);
        // Handle the error and update the UI accordingly
    });
}

function deleteFile(fileId, fileName) {
    fetch(`${BASE_URL}/${fileId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            console.log('File deleted successfully:', data.message);
            toastr.success(`${fileName} deleted successfully`)
            location.reload();
        } else {
            console.error('Error deleting file:', data.error);
            toastr.error(`Error deleting file ${fileName}`)
            //TODO: Implement handling the error and updating the UI accordingly
        }
    })
    .catch(error => {
        console.error('Error deleting file:', error);
        toastr.error(`Error deleting file ${fileName}`)
        //TODO: Implement handling the error and updating the UI accordingly
    });
}

function renameFile(fileId) {
    // Set the fileId to the hidden input field
    document.getElementById('hiddenFileId').value = fileId;
    // Open the rename modal //
    $('#renameModal').modal('show');
}

function reuploadFile(fileId) {
    // Set the fileId to the hidden input field
    document.getElementById('hiddenFileId').value = fileId;
    // Open the rename modal //
    $('#reuploadModal').modal('show');
}

function submitRename() {
    const newFileName = document.getElementById('newFileName').value;
    const fileId = document.getElementById('hiddenFileId').value;

    // Check if the user has entered file name
    if (newFileName.trim() === '') {
        toastr.error('Please enter file name');
        return;
    }

    const formData = new FormData();
    formData.append('file_name', newFileName);

    fetch(`${BASE_URL}/${fileId}`, {
        method: 'PUT',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            console.log('File name updated successfully:', data.message);
            location.reload();
        } else {
            console.error('Error updating file name:', data.error);
            toastr.error(`Error updating file name to ${newFileName}`)
            //TODO: Implement handling the error and updating the UI accordingly
        }
    })
    .catch(error => {
        console.error('Error updating file name:', error);
        toastr.error(`Error updating file name to ${newFileName}`)
        //TODO: Implement handling the error and updating the UI accordingly
    });

    // Close the rename modal
    $('#renameModal').modal('hide');
}

function submitReupload() {
    // Get the fileId from the hidden input field
    const fileId = document.getElementById('hiddenFileId').value;

    // Get the file input element
    const fileInput = document.getElementById('reuploadFile');

    // Check if a file is selected
    if (!fileInput.files || fileInput.files.length === 0) {
        toastr.error('Please choose a file to reupload.');
        return;
    }

    // Get the selected file
    const reuploadFile = fileInput.files[0];

    // Create a FormData object and append the file
    const formData = new FormData();
    formData.append('file', reuploadFile);

    // Add your logic to handle the API call to update the file
    fetch(`http://localhost:5000/api/v1/files/${fileId}`, {
        method: 'PUT',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status) {
            console.log('File reuploaded successfully:', data.message);
            location.reload();
        } else {
            console.error('Error reuploading file:', data.error);
            toastr.error('Error reuploading file')
            //TODO: Implement handling the error and updating the UI accordingly
        }
    })
    .catch(error => {
        console.error('Error reuploading file:', error);
        toastr.error('Error reuploading file')
        //TODO: Implement handling the error and updating the UI accordingly
    });

    // Close the reupload modal
    $('#reuploadModal').modal('hide');
}


function populateFileList(files) {
    const fileListTable = document.getElementById('fileListTable');
    const tbody = fileListTable.querySelector('tbody');

    tbody.innerHTML = ''; // Clear existing rows

    files.forEach(file => {
        const row = tbody.insertRow();

        row.insertCell(0).textContent = file.file_name;
        row.insertCell(1).textContent = convertUtcToIst(file.created_at);
        row.insertCell(2).textContent = convertUtcToIst(file.updated_at);
        row.insertCell(3).textContent = formatFileSize(file.size_in_bytes);
        row.insertCell(4).textContent = file.file_type;
        
        // Add a cell with three dots and a dropdown
        const actionsCell = row.insertCell(5);
        const actionsButton = document.createElement('button');
        actionsButton.textContent = '⋮'; // Three dots character
        actionsButton.classList.add('dropdown-btn');

        // Create a dropdown content
        const dropdownContent = document.createElement('div');
        dropdownContent.classList.add('dropdown-content');

        const downloadOption = document.createElement('a');
        downloadOption.textContent = 'Download';
        downloadOption.onclick = function () {
            downloadFile(file._id);
        };
        dropdownContent.appendChild(downloadOption);

        const renameOption = document.createElement('a');
        renameOption.textContent = 'Rename';
        renameOption.onclick = function () {
            renameFile(file._id);
        };
        dropdownContent.appendChild(renameOption);

        const reuploadOption = document.createElement('a');
        reuploadOption.textContent = 'Reupload';
        reuploadOption.onclick = function () {
            reuploadFile(file._id);
        };
        dropdownContent.appendChild(reuploadOption);

        const deleteOption = document.createElement('a');
        deleteOption.textContent = 'Delete';
        deleteOption.onclick = function () {
            deleteFile(file._id, file.file_name);
        };
        dropdownContent.appendChild(deleteOption);

        actionsButton.appendChild(dropdownContent);
        actionsCell.appendChild(actionsButton);
    });
}

function initiateFileDownload(signedUrl) {
    const downloadLink = document.createElement('a');
    downloadLink.style.display = 'none';
    downloadLink.href = signedUrl;

    downloadLink.setAttribute('download', 'downloaded-file');

    // Trigger a click on the link to start the download //
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);
}

function formatFileSize(bytes) {
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 Byte';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(1) + ' ' + sizes[i];
}

function convertUtcToIst(utcTimestamp) {
    const utcDate = new Date(utcTimestamp);
    const istDate = new Date(utcDate.getTime() + 5.5 * 60 * 60 * 1000);

    // Format the date and time
    const formattedDate = istDate.toLocaleDateString('en-US', {
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
    });

    const formattedTime = istDate.toLocaleTimeString('en-US', {
        timeZone: 'Asia/Kolkata',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
    });

    const istDateTime = `${formattedDate} ${formattedTime}`;
    return istDateTime;
}