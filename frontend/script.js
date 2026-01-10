function uploadDocument() {
    const fileInput = document.getElementById('document');
    const result = document.getElementById('result');

    if (fileInput.files.length === 0) {
        result.innerText = "Please select a file.";
        return;
    }

    const formData = new FormData();
    formData.append('document', fileInput.files[0]);

    fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        result.innerText = data.message;
    })
    .catch(error => {
        result.innerText = "Error uploading file";
        console.error(error);
    });
}
