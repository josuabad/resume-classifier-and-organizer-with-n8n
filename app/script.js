document.addEventListener("DOMContentLoaded", () => {
  const applyForm = document.getElementById("applyForm");
  const cvFileInput = document.getElementById("cvFile");
  const fileNameSpan = document.getElementById("fileName");
  const responseMessage = document.getElementById("responseMessage");

  // Actualizar texto cuando el usuario selecciona un archivo
  cvFileInput.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
      fileNameSpan.textContent = `Archivo: ${e.target.files[0].name}`;
    } else {
      fileNameSpan.textContent = "Haz clic para seleccionar tu CV (PDF o DOCX)";
    }
  });

  // Enviar formulario (únicamente vacancy_id y cv)
  applyForm.addEventListener("submit", async (e) => {
    e.preventDefault();

    const vacancyId = document.getElementById("vacancyId").value;
    const cvFile = cvFileInput.files[0];

    if (!cvFile) return;

    const formData = new FormData();
    formData.append("vacancy_id", vacancyId);
    formData.append("cv", cvFile);

    try {
      const response = await fetch("/postular", {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        showMessage(`Enviado con éxito. ID Vacante: ${data.vacancy_id}`, true);
        applyForm.reset();
        fileNameSpan.textContent =
          "Haz clic para seleccionar tu CV (PDF o DOCX)";
      } else {
        showMessage("Error al procesar la solicitud.", false);
      }
    } catch (err) {
      showMessage("No se pudo conectar con el servidor.", false);
    }
  });

  function showMessage(msg, isSuccess) {
    responseMessage.textContent = msg;
    responseMessage.className = `message ${isSuccess ? "success" : "error"}`;
  }
});
