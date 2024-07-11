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

    fetch("/upload/", {
      method: "POST",
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

  // Event handler for when the modal is closed
  $("#uploadModal").on("hidden.bs.modal", function () {
    // Clear the job description text area
    jobDescription.value = "";

    // Clear the file input
    resumeFolder.value = "";

    // Reset the upload button text and visibility
    uploadBtn.style.display = "block";
    uploadBtn.textContent = "Upload";
    uploadBtn.disabled = true;

    // Remove the download button if it exists
    var downloadButton = document.querySelector(".modal-footer a");
    if (downloadButton) {
      downloadButton.remove();
    }
  });
});