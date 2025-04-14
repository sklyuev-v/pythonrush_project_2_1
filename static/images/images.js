let currentPage = 1;
const imagesPerPage = 9;
const closeBtn = document.getElementById("close");
const imagesContainer = document.getElementById("images_placeholder");

function setImages(images) {
  const modal = document.getElementById("modal");
  const modalImg = document.getElementById("modal-img");

  let count = 0;
  images.forEach((image) => {
    const fullFilename = image.filename + image.file_type;
    const mainDivEl = document.createElement("div");
    mainDivEl.className = "col m-2 rounded";
    mainDivEl.style.width = "310px";
    mainDivEl.style.height = "200px";
    imagesContainer.appendChild(mainDivEl);

    const imageDivEl = document.createElement("div");
    imageDivEl.className = "col m-2 rounded";
    imageDivEl.style.width = "300px";
    imageDivEl.style.height = "170px";
    mainDivEl.appendChild(imageDivEl);

    //const aElement = document.createElement("a");
    //aElement.href = `/images/${fullFilename}`;
    //imageDivEl.appendChild(aElement);

    const imageElement = document.createElement("img");
    imageElement.src = `/images/${fullFilename}`;
    imageElement.alt = image;
    imageElement.id = "image" + count;
    imageElement.style.height = "100%";
    imageElement.style.width = "auto";
    imageElement.addEventListener("click", () => {
      modalImg.src = `/images/${fullFilename}`;
      modal.style.display = "block";
    });
    imageDivEl.appendChild(imageElement);
    //aElement.appendChild(imageElement);

    const buttonDivEl = document.createElement("div");
    buttonDivEl.className = "col m-2 rounded";
    buttonDivEl.style.width = "310px";
    buttonDivEl.style.height = "30px";
    mainDivEl.appendChild(buttonDivEl);

    const buttonCopyLink = document.createElement("button");
    buttonCopyLink.textContent = "Скопировать ссылку";
    buttonCopyLink.className = "btn btn-secondary me-2 btn-sm px-2";
    buttonCopyLink.onclick = () => {
      navigator.clipboard
        .writeText(window.location.origin + "/images/" + fullFilename)
        .then(() => {
          alert("Ссылка скопирована в буфер обмена!");
        })
        .catch((err) => {
          alert("Ошибка при копировании ссылки: " + err);
        });
    };
    buttonDivEl.appendChild(buttonCopyLink);

    const buttonDownload = document.createElement("button");
    buttonDownload.textContent = "Загрузить";
    buttonDownload.className = "btn btn-secondary btn-sm px-2";
    buttonDownload.onclick = () => {
      const link = document.createElement("a");
      link.href = `/images/${fullFilename}`;
      link.download = fullFilename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    };
    buttonDivEl.appendChild(buttonDownload);

    count++;
    count = count > 2 ? 0 : count;
  });
}

function loadImages(page) {
  fetch(`/api/images/?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      imagesContainer.innerHTML = "";
      if (data.images.length == 0) {
        const notImagesText = document.createElement("h2");
        notImagesText.textContent = "Нет загруженных изображений";
        imagesContainer.appendChild(notImagesText);
      } else {
        setImages(data.images);
        document.getElementById("nextPage").disabled =
          data.images.length < imagesPerPage;
        document.getElementById("prevPage").disabled = page === 1;
        document.getElementById("currentPage").textContent = page;
        currentPage = page;
      }
    });
}

document.getElementById("prevPage").addEventListener("click", () => {
  if (currentPage > 1) {
    loadImages(currentPage - 1);
  }
});

document.getElementById("nextPage").addEventListener("click", () => {
  loadImages(currentPage + 1);
});

loadImages(1);

closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
});

modal.addEventListener("click", () => {
  modal.style.display = "none";
});
