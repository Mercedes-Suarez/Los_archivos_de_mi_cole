let currentImage = 0;
const slides = document.querySelectorAll('.slide-img');
if (slides.length > 0) {
    slides[currentImage].style.display = 'block';
    setInterval(() => {
        slides[currentImage].style.display = 'none';
        currentImage = (currentImage + 1) % slides.length;
        slides[currentImage].style.display = 'block';
    }, 4000);
}
