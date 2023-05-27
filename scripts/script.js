function load() {
  document.addEventListener("DOMContentLoaded", function() {
    const carouselItems = document.querySelectorAll(".carousel-item");
    const prevBtn = document.querySelector(".prev-btn");
    const nextBtn = document.querySelector(".next-btn");
    let currentIndex = 0;
  
    function showCurrentSlide() {
      carouselItems.forEach(function(item) {
        item.classList.remove("active");
      });
      carouselItems[currentIndex].classList.add("active");
    }
  
    function goToNextSlide() {
      currentIndex++;
      if (currentIndex >= carouselItems.length) {
        currentIndex = 0;
      }
      showCurrentSlide();
    }
  
    function goToPrevSlide() {
      currentIndex--;
      //check if the current index is less than zero
      if (currentIndex < 0) {
        currentIndex = carouselItems.length - 1;
      }
      //show current
      showCurrentSlide();
    }
  
    prevBtn.addEventListener("click", goToPrevSlide);
    nextBtn.addEventListener("click", goToNextSlide);
  
    // Initialize the carousel by showing the first slide
    showCurrentSlide();
  });

//carousel function(might delete)
  
}