function previewImage(event) {
    const imagePreview = document.getElementById('imagePreview');
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreview.style.display = 'block'; // Show the image
        };
        reader.readAsDataURL(file);
        
        // Reset prediction result when a new image is selected
        document.querySelector('.result').style.display = 'none'; // Hide previous prediction results
    } else {
        imagePreview.src = '';
        imagePreview.style.display = 'none'; // Hide the image if no file is selected
    }
}
