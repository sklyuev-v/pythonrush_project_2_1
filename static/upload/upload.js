let input = document.querySelector(".input");
let preview = document.querySelector(".preview");
let loadBtn = document.getElementById("loadBtn");

input.addEventListener("change", updateImageDisplay);
loadBtn.addEventListener("click", () => {
  uploadFile();
});
loadBtn.disabled = true;

function updateImageDisplay() {
  while (preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  const curFile = input.files[0];

  if (!curFile) {
    let text = document.createElement("p");
    text.textContent = "Не выбран файл для загрузки";
    preview.appendChild(text);
  } else {
    const previewDivEl = document.createElement("div");
    preview.appendChild(previewDivEl);

    let filenamePEl = document.createElement("p");
    filenamePEl.className = "mb-0";
    filenamePEl.id = "filename";

    let filesizePEl = document.createElement("p");

    if (validFileType(curFile)) {
      loadBtn.disabled = false;
      filenamePEl.textContent = `Имя: ${curFile.name}`;
      filesizePEl.textContent = `Размер: ${returnFileSize(curFile.size)}`;

      let imageElement = document.createElement("img");
      imageElement.id = "previewImage";
      imageElement.src = window.URL.createObjectURL(curFile);
      imageElement.style.width = "100%";
      imageElement.style.height = "auto";

      previewDivEl.appendChild(imageElement);
      previewDivEl.appendChild(filenamePEl);
      previewDivEl.appendChild(filesizePEl);
    } else {
      filenamePEl.textContent = `Имя: ${curFile.name}`;
      filesizePEl.textContent = "Неверный тип файла. Выберите другой.";
      previewDivEl.appendChild(filenamePEl);
      previewDivEl.appendChild(filesizePEl);
      loadBtn.disabled = true;
    }
  }
}

const fileTypes = ["image/jpeg", "image/jpg", "image/gif", "image/png"];

function validFileType(file) {
  return fileTypes.includes(file.type);
}

function returnFileSize(number) {
  if (number < 1024) {
    return number + "bytes";
  } else if (number > 1024 && number < 1048576) {
    return (number / 1024).toFixed(1) + "KB";
  } else if (number > 1048576) {
    return (number / 1048576).toFixed(1) + "MB";
  }
}

function uploadFile() {
  const file = input.files[0];
  if (!file) return alert("Выберите файл для загрузки.");

  fetch("/api/upload/", {
    method: "POST",
    headers: {
      Filename: file.name,
    },
    body: file,
  })
    .then((response) => {
      loadBtn.textContent = "Успешно загружено";
      loadBtn.disabled = true;

      file_location = response.headers.get("Location");
      filename = response.headers.get("Filename");

      document.getElementById("filename").textContent = filename;

      downloadButton = document.getElementById("downBtn");
      downloadButton.hidden = false;
      downloadButton.onclick = () => {
        const link = document.createElement("a");
        link.href = `/images/${filename}`;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };

      copyLinkButton = document.getElementById("copyBtn");
      copyLinkButton.hidden = false;
      copyLinkButton.onclick = () => {
        navigator.clipboard
          .writeText(file_location + filename)
          .then(() => {
            alert("Ссылка скопирована в буфер обмена!");
          })
          .catch((err) => {
            alert("Ошибка при копировании ссылки: " + err);
          });
      };
    })
    .catch((error) => {
      console.error("Ошибка загрузки:", error);
    });
}
