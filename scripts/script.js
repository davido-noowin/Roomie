const buttons = document.querySelectorAll('.carousel-button[data-carousel-button]');
buttons.forEach(button => {
  button.addEventListener('click', () => {
    const offset = button.dataset.carouselButton === 'next' ? 1 : -1;
    const carousel = button.closest('.carousel');
    const slides = carousel.querySelectorAll('.slide');

    const activeSlide = carousel.querySelector('.slide[data-active]');
    let newIndex = Array.from(slides).indexOf(activeSlide) + offset;
    if (newIndex < 0) newIndex = slides.length - 1;
    if (newIndex >= slides.length) newIndex = 0;

    activeSlide.removeAttribute('data-active');
    slides[newIndex].setAttribute('data-active', 'true');
  });
});
function openPopup() {
  document.getElementById('popup').classList.add("open-popup");
}

function closePopup() {
  document.getElementById('popup').classList.remove("open-popup");
}


