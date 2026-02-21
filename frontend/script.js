document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.getElementById("fileInput");
    const previewContainer = document.getElementById("previewContainer");
    const imagePreview = document.getElementById("imagePreview");

    fileInput.addEventListener("change", function () {

        const file = this.files[0];

        if (!file) {
            previewContainer.style.display = "none";
            imagePreview.src = "";
            previewContainer.innerHTML = "";
            return;
        }

        const fileType = file.type;

        // Clear previous preview
        previewContainer.innerHTML = "";
        previewContainer.style.display = "block";

        // 🖼 IMAGE PREVIEW
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

        // 📄 PDF PREVIEW
        else if (fileType === "application/pdf") {

            const reader = new FileReader();

            reader.onload = function (e) {
                const embed = document.createElement("embed");
                embed.src = e.target.result;
                embed.type = "application/pdf";
                embed.width = "100%";
                embed.height = "500px";
                embed.style.borderRadius = "10px";
                previewContainer.appendChild(embed);
            };

            reader.readAsDataURL(file);
        }

        else {
            alert("Unsupported file type. Please upload Image or PDF.");
            previewContainer.style.display = "none";
        }

    });

});