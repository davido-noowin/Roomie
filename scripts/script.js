function load() {
  document.addEventListener("DOMContentLoaded", function() {
    const carouselItems = document.querySelectorAll(".carousel-item");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    let currentIndex = 0;
  
    buttons.forEach(button => {
      button.addEventListener("click", () => {
        const offset = button.dataset.carouselButton === "next" ? 1 : -1
        const slides = button.closest("[data-carousel]").querySelector("[data-slides")
      })
    })
  }
}
