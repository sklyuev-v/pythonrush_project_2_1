
let input = document.querySelector(".input");
let preview = document.querySelector(".preview");
let submit = document.querySelector(".submit")
console.log(submit.textContent)
submit.disabled = true;


input.addEventListener("change", updateImageDisplay);

function updateImageDisplay() {
  while (preview.firstChild) {
    preview.removeChild(preview.firstChild);
  }

  let curFiles = input.files;
  if (curFiles.length === 0) {
    var para = document.createElement("p");
    para.textContent = "Не выбран файл для загрузки";
    preview.appendChild(para);
  } else {
    const divElement = document.createElement("div");
    preview.appendChild(divElement);
    
    for (let i=0; i < curFiles.length; i++) {
      let pElement = document.createElement("p");
      let spanElement = document.createElement("span");
      let p2Element = document.createElement("p");
      if (validFileType(curFiles[i])) {
        submit.disabled = false;
        pElement.textContent = `Имя: ${curFiles[i].name}`;
        p2Element.textContent = `Размер: ${returnFileSize(curFiles[i].size)}`;

        let imageElement = document.createElement("img");
        imageElement.src = window.URL.createObjectURL(curFiles[i]);
        imageElement.style.width = "100%";
        imageElement.style.height = "auto";

        divElement.appendChild(imageElement);
        divElement.appendChild(spanElement);
        divElement.appendChild(pElement);
        divElement.appendChild(spanElement);
        divElement.appendChild(p2Element);
      } else {
        pElement.textContent = `Имя: ${curFiles[i].name}`;
        p2Element.textContent = "Неверный тип файла. Выберите другой.";
        divElement.appendChild(pElement);
        divElement.appendChild(spanElement);
        divElement.appendChild(p2Element);
        submit.disabled = true;

      }
    }

  }
}

var fileTypes = ["image/jpeg", "image/pjpeg", "image/png"];

function validFileType(file) {
  for (var i = 0; i < fileTypes.length; i++) {
    if (file.type === fileTypes[i]) {
      return true;
    }
  }

  return false;
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
;
        