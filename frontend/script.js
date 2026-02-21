document.addEventListener("DOMContentLoaded", function () {

    const form = document.getElementById("uploadForm");
    const fileInput = document.getElementById("fileInput");
    const previewContainer = document.getElementById("previewContainer");
    const resultBox = document.getElementById("result");

    // =========================
    // FILE PREVIEW SECTION
    // =========================
    fileInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            previewContainer.style.display = "none";
            previewContainer.innerHTML = "";
            return;
        }

        previewContainer.innerHTML = "";
        previewContainer.style.display = "block";

        const fileType = file.type;

        // IMAGE PREVIEW
        if (fileType.startsWith("image/")) {

            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement("img");
                img.src = e.target.result;
                img.style.maxWidth = "100%";
                img.style.maxHeight = "400px";
                img.style.borderRadius = "10px";
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        }

        // PDF PREVIEW
        else if (fileType === "application/pdf") {

            const reader = new FileReader();
            reader.onload = function (e) {
                const embed = document.createElement("embed");
                embed.src = e.target.result;
                embed.type = "application/pdf";
                embed.width = "100%";
                embed.height = "500px";
                previewContainer.appendChild(embed);
            };
            reader.readAsDataURL(file);
        }

        else {
            alert("Unsupported file type. Upload image or PDF only.");
            previewContainer.style.display = "none";
        }
    });

    // =========================
    // FORM SUBMISSION (POST)
    // =========================
    form.addEventListener("submit", function (e) {
        e.preventDefault();

        const formData = new FormData();
        const file = fileInput.files[0];

        if (!file) {
            alert("Please select a file.");
            return;
        }

        formData.append("file", file);

        resultBox.innerHTML = "Processing...";
        resultBox.style.display = "block";

        fetch("http://127.0.0.1/5000/predict", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {

            if (data.error) {
                resultBox.innerHTML = "Error: " + data.error;
                resultBox.style.color = "red";
            } else {
                resultBox.innerHTML = `
                    <h3>Prediction: ${data.prediction}</h3>
                    <p>Confidence: ${data.confidence}%</p>
                `;

                resultBox.style.color =
                    data.prediction.toLowerCase() === "forged"
                    ? "red"
                    : "green";
            }

        })
        .catch(error => {
            resultBox.innerHTML = "Error occurred while processing.";
            resultBox.style.color = "red";
        });
    });

});