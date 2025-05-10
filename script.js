async function predict(imageFile) {
    const formData = new FormData();
    formData.append('image', imageFile);

    try {
        const response = await fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const blob = await response.blob();
            const imageUrl = URL.createObjectURL(blob);
            return imageUrl;
        } else {
            throw new Error('Renkli fotoğraf oluşturulamadı.');
        }
    } catch (error) {
        throw new Error('Hata: ' + error.message);
    }
}

function handleFiles(files) {
    const file = files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        predict(file).then(imageUrl => {
            const resultsContainer = document.getElementById('results');
            const imgElement = document.createElement('img');
            imgElement.src = imageUrl;
            resultsContainer.appendChild(imgElement);
            resultsContainer.style.display = 'block';
        }).catch(error => {
            console.error(error);
        });
    };
    reader.readAsDataURL(file);
}
