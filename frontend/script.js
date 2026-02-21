function uploadImage() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    // =========================
    // 🔎 IMAGE PREVIEW SECTION
    // =========================
    const previewContainer = document.getElementById("previewContainer");
    previewContainer.style.display = "block";
    previewContainer.innerHTML = `
        <img src="${URL.createObjectURL(file)}" 
             style="max-width:300px; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
    `;

    // =========================
    // 📡 SEND TO BACKEND
    // =========================
    const formData = new FormData();
    formData.append("file", file);

    document.getElementById("loading").style.display = "block";
    document.getElementById("resultBox").style.display = "none";

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {

        document.getElementById("loading").style.display = "none";
        document.getElementById("resultBox").style.display = "block";

        document.getElementById("cnnPrediction").innerText = data.cnn_decision;
        document.getElementById("cnnConfidence").innerText = data.cnn_score;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("loading").style.display = "none";
        alert("Something went wrong.");
    });
}