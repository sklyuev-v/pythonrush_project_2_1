fetch("/api/images")
  .then((response) => response.json())
  .then((data) => {
    const imagesContainer = document.getElementById("images_placeholder");
    let count = 0;
    data.images.forEach((image) => {
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

      const aElement = document.createElement("a");
      aElement.href = `/images/${image}`;
      imageDivEl.appendChild(aElement);

      const imageElement = document.createElement("img");
      imageElement.src = `/images/${image}`;
      imageElement.alt = image;
      imageElement.id = "image" + count;
      imageElement.style.height = "100%";
      imageElement.style.width = "auto";
      aElement.appendChild(imageElement);

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
          .writeText(window.location.origin + "/images/" + image)
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
        link.href = `/images/${image}`;
        link.download = image;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
      };
      buttonDivEl.appendChild(buttonDownload);

      count++;
      count = count > 2 ? 0 : count;
    });
  });
