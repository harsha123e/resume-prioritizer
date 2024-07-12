document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.getElementById("uploadBtn");
    const jobDescription = document.getElementById("jobDescription");
    const resumeFolder = document.getElementById("resumeFolder");

    function validateForm() {
        if (jobDescription.value.trim() !== "" && resumeFolder.files.length > 0) {
            uploadBtn.disabled = false;
        } else {
            uploadBtn.disabled = true;
        }
    }

    jobDescription.addEventListener("input", validateForm);
    resumeFolder.addEventListener("change", validateForm);

    document.getElementById("uploadBtn").addEventListener("click", function () {
        uploadBtn.textContent = "Processing...";

        var jobDescriptionValue = jobDescription.value;
        var resumeFiles = resumeFolder.files;

        var formData = new FormData();
        formData.append("jobDescription", jobDescriptionValue);
        for (var i = 0; i < resumeFiles.length; i++) {
            formData.append("resumeFolder", resumeFiles[i]);
        }

        var csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
        fetch("/upload/", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
            },
            body: formData,
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.blob();
            })
            .then((blob) => {
                var url = URL.createObjectURL(blob);
                var downloadButton = document.createElement("a");
                downloadButton.href = url;
                downloadButton.download = "ranked_resumes.zip";
                downloadButton.textContent = "Download Ranked Resumes";
                downloadButton.classList.add("btn", "btn-primary");

                var modalFooter = document.querySelector(".modal-footer");
                modalFooter.appendChild(downloadButton);
                uploadBtn.style.display = "none";
            })
            .catch((error) => {
                console.error("Error:", error);
                uploadBtn.textContent = "Upload";
            });
    });

    $("#uploadModal").on("hidden.bs.modal", function () {
        jobDescription.value = "";
        resumeFolder.value = "";
        uploadBtn.style.display = "block";
        uploadBtn.textContent = "Upload";
        uploadBtn.disabled = true;

        var downloadButton = document.querySelector(".modal-footer a");
        if (downloadButton) {
            downloadButton.remove();
        }
    });

    document.getElementById("loadDemoDataBtn").addEventListener("click", function () {
        fetch("/load-demo-data/")
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Failed to load demo data");
                }
                return response.json();
            })
            .then((data) => {
                jobDescription.value = data.job_description;

                const dataTransfer = new DataTransfer();

                data.resume_files.forEach((resume) => {
                    const byteCharacters = atob(resume.content);
                    const byteNumbers = new Array(byteCharacters.length);
                    for (let i = 0; i < byteCharacters.length; i++) {
                        byteNumbers[i] = byteCharacters.charCodeAt(i);
                    }
                    const byteArray = new Uint8Array(byteNumbers);
                    const file = new File([byteArray], resume.filename, { type: 'application/pdf' });
                    dataTransfer.items.add(file);
                });

                resumeFolder.files = dataTransfer.files;

                validateForm();
            })
            .catch((error) => {
                console.error("Error loading demo data:", error);
            });
    });
});
