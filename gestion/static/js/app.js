// Carrusel de frases motivacionales
let currentText = 0;
const textSlides = document.querySelectorAll('.carousel .slide');

function showText(index) {
    textSlides.forEach((slide, i) => {
        slide.classList.remove('active');
        if (i === index) slide.classList.add('active');
    });
}

if (textSlides.length > 0) {
    showText(currentText);
    setInterval(() => {
        currentText = (currentText + 1) % textSlides.length;
        showText(currentText);
    }, 4000);
}
