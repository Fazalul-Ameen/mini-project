function uploadDocument() {  //Document upload function
    const fileInput = document.getElementById('document');
    const result = document.getElementById('result');

    if (fileInput.files.length === 0) {  //if no file is selected
        result.innerText = "Please select a file.";
        return;
    }

    const formData = new FormData(); //Creating FormData object to send file
    formData.append('document', fileInput.files[0]);

    fetch('http://127.0.0.1:5000/upload', { //sending the file to backend.
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        result.innerText = data.message;
    })
    .catch(error => { //If any error occurs
        result.innerText = "Error uploading file";
        console.error(error);
    });
}

// File Preview Functionality
const fileInput = document.getElementById("document");
const previewContainer = document.getElementById("previewContainer");

previewContainer.style.display="none";

fileInput.addEventListener("change", function () {
    previewContainer.innerHTML = "";
    previewContainer.style.display="block";
    const file = this.files[0];
    if (!file) return;

    // File name
    const fileInfo = document.createElement("p");
    fileInfo.innerText = `Selected File: ${file.name}`;
    previewContainer.appendChild(fileInfo);

    // IMAGE PREVIEW
    if (file.type.startsWith("image/")) {
        const img = document.createElement("img");
        img.style.maxWidth = "300px";
        img.style.marginTop = "10px";

        const reader = new FileReader();
        reader.onload = function (e) {
            img.src = e.target.result;
        };

        reader.readAsDataURL(file);
        previewContainer.appendChild(img);
    }

    // PDF PREVIEW
    else if (file.type === "application/pdf") {
        const pdfPreview = document.createElement("embed");
        pdfPreview.src = URL.createObjectURL(file);
        pdfPreview.type = "application/pdf";
        pdfPreview.width = "100%";
        pdfPreview.height = "400px";

        previewContainer.appendChild(pdfPreview);
    }

    // Unsupported file
    else {
        const msg = document.createElement("p");
        msg.innerText = "Preview not available for this file type.";
        previewContainer.appendChild(msg);
    }
});
