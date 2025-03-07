document.querySelector(".copyButton").addEventListener("click", function() {
    navigator.clipboard.writeText(document.querySelector(".imageLink").src).then(function() {
        alert('Ссылка на изображение скопирована')
    }).catch(function(error) {
        console.error('Error:', error);
    });
});