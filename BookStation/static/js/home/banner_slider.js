document.addEventListener("DOMContentLoaded", function () {
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const prevButton = document.querySelector('.prev');
  const nextButton = document.querySelector('.next');
  
  // Tạo container chứa dot (nếu chưa có trong HTML)
  let dotsContainer = document.querySelector('.dots');
  if (!dotsContainer) {
    dotsContainer = document.createElement('div');
    dotsContainer.classList.add('dots');
    document.querySelector('.banner-slider').appendChild(dotsContainer);
  }

  // Tạo dot cho từng slide
  slides.forEach((_, i) => {
    const dot = document.createElement('span');
    dot.classList.add('dot');
    if(i === 0) dot.classList.add('active');
    dot.addEventListener('click', () => {
      currentSlide = i;
      showSlide(currentSlide);
      resetInterval();
    });
    dotsContainer.appendChild(dot);
  });

  const dots = document.querySelectorAll('.dot');

  function showSlide(index) {
    slides.forEach((slide, i) => {
      slide.classList.toggle('active', i === index);
      dots[i].classList.toggle('active', i === index);
    });
  }

  function nextSlide() {
    currentSlide = (currentSlide + 1) % slides.length;
    showSlide(currentSlide);
  }

  function prevSlide() {
    currentSlide = (currentSlide - 1 + slides.length) % slides.length;
    showSlide(currentSlide);
  }

  nextButton.addEventListener('click', () => {
    nextSlide();
    resetInterval();
  });

  prevButton.addEventListener('click', () => {
    prevSlide();
    resetInterval();
  });

  // Tự động chuyển slide sau 5s, có reset khi người dùng thao tác
  let slideInterval = setInterval(nextSlide, 5000);

  function resetInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
  }

  // Hiển thị slide đầu tiên
  showSlide(currentSlide);
});
