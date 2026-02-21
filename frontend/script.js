const fileInput = document.getElementById("fileInput");
const previewImage = document.getElementById("previewImage");
const loading = document.getElementById("loading");
const resultBox = document.getElementById("resultBox");

// Preview selected image
fileInput.addEventListener("change", function () {
    const file = this.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewImage.style.display = "block";
        };
        reader.readAsDataURL(file);
    }
});


// Upload image to Flask backend
function uploadImage() {

    const file = fileInput.files[0];

    if (!file) {
        alert("Please select an image first!");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    loading.style.display = "block";
    resultBox.style.display = "none";

    fetch('http://127.0.0.1:5000/predict', {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
   .then(data => {

    console.log("Response:", data);

    loading.style.display = "none";
    resultBox.style.display = "block";

    document.getElementById("cnnPrediction").innerText = data.cnn_decision;
    document.getElementById("cnnConfidence").innerText = data.cnn_score;

    document.getElementById("ruleScore").innerText = data.keywords_found ? "Keywords Found" : "No Keywords";
    document.getElementById("ruleDecision").innerText = data.aadhaar_number ? "Aadhaar Detected" : "No Aadhaar";

    const finalDecision = document.getElementById("finalDecision");
    finalDecision.innerText = data.cnn_decision;

    if (data.cnn_decision.toLowerCase().includes("forged")) {
        finalDecision.style.color = "red";
    } else {
        finalDecision.style.color = "lime";
    }

})
    .catch(error => {
        loading.style.display = "none";
        alert("Error occurred while processing.");
        console.error("Error:", error);
    });
}
