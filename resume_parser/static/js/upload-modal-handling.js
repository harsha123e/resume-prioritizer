document.getElementById("uploadBtn").addEventListener("click", function () {
  var uploadBtn = document.getElementById("uploadBtn");
  uploadBtn.textContent = "Processing...";

  var jobDescription = document.getElementById("jobDescription").value;
  var resumeFolder = document.getElementById("resumeFolder").files;

  var formData = new FormData();
  formData.append("jobDescription", jobDescription);
  for (var i = 0; i < resumeFolder.length; i++) {
    formData.append("resumeFolder", resumeFolder[i]);
  }

  // Add a delay of 3 seconds before proceeding with the fetch request
  setTimeout(function () {
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
  }, 3000); // 3-second delay
});

// Event handler for when the modal is closed
$("#uploadModal").on("hidden.bs.modal", function () {
  // Clear the job description text area
  document.getElementById("jobDescription").value = "";

  // Clear the file input
  document.getElementById("resumeFolder").value = "";

  // Reset the upload button text and visibility
  var uploadBtn = document.getElementById("uploadBtn");
  uploadBtn.style.display = "block";
  uploadBtn.textContent = "Upload";

  // Remove the download button if it exists
  var downloadButton = document.querySelector(".modal-footer a");
  if (downloadButton) {
    downloadButton.remove();
  }
});
