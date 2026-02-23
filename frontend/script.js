function uploadImage() {

    const fileInput = document.getElementById("fileInput");
    const file = fileInput.files[0];

    if (!file) {
        alert("Please select a file first.");
        return;
    }

    // =========================
    // 🔎 IMAGE + PDF PREVIEW SECTION   
    // =========================
    const previewContainer = document.getElementById("previewContainer");
    previewContainer.style.display = "block";

    const fileURL = URL.createObjectURL(file);

    if (file.type === "application/pdf") {

        previewContainer.innerHTML = `
            <embed src="${fileURL}" 
                   type="application/pdf"
                   width="100%" 
                   height="400px"
                   style="border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
        `;

    } else {

        previewContainer.innerHTML = `
            <img src="${fileURL}" 
                 style="max-width:300px; border-radius:8px; box-shadow:0 4px 8px rgba(0,0,0,0.2);">
        `;
    }

    // =========================
    // 📡 SEND TO BACKEND (UNCHANGED)
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

        console.log(data);

        document.getElementById("loading").style.display = "none";
        document.getElementById("resultBox").style.display = "block";

        document.getElementById("cnnPrediction").innerText = data.cnn_prediction;
        document.getElementById("cnnConfidence").innerText = data.cnn_confidence;
        document.getElementById("ruleScore").innerText = data.rule_score;
        document.getElementById("ruleDecision").innerText = data.rule_decision;
        const result = document.getElementById("finalDecision").innerText = data.final_decision;
        if(result === "Forged"){
            document.getElementById("finalDecision").style.color = "#ff4d4d";
        }
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("loading").style.display = "none";
        alert("Something went wrong.");
    });

}