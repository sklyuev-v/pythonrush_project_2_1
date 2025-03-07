fetch('http://localhost:8000/images')
    .then(response => response.json())
    .then(data => {
        const imagesContainer = document.getElementById('images_placeholder');
        let count = 0;
        data.images.forEach(image => {
            const divElement = document.createElement('div')
            divElement.className = 'col m-2 rounded' 
            divElement.style.width = '300px';
            divElement.style.height = '170px';
            imagesContainer.appendChild(divElement)

            const aElement = document.createElement('a');
            aElement.href = `/images/${image}`;
            divElement.appendChild(aElement);

            const imageElement = document.createElement('img');
            imageElement.src = `/images/${image}`;
            imageElement.alt = image;
            imageElement.style.height = '100%';
            imageElement.style.width = 'auto';
            aElement.appendChild(imageElement);

            count++;
            count = count > 2 ? 0 : count;
        });
    })



