document.addEventListener("DOMContentLoaded", function () {
  // Thiết lập biến
  let currentSlide = 0;
  const slides = document.querySelectorAll('.slide');
  const totalSlides = slides.length;
  const prevButton = document.querySelector('.prev');
  const nextButton = document.querySelector('.next');
  let isAnimating = false;

  // Tạo điểm chỉ báo (dots)
  createDots();
  
  // Khởi tạo slider
  initSlider();

  // Khởi tạo slider với slide đầu tiên active
  function initSlider() {
    // Ẩn tất cả slide
    slides.forEach((slide) => {
      slide.classList.remove('active', 'previous', 'next');
    });
    
    // Hiển thị slide hiện tại
    slides[currentSlide].classList.add('active');
    
    // Cập nhật dots
    updateDots();
  }

  // Tạo dots cho slider
  function createDots() {
    const dotsContainer = document.querySelector('.dots');
    dotsContainer.innerHTML = '';

    slides.forEach((_, index) => {
      const dot = document.createElement('span');
      dot.classList.add('dot');
      if (index === currentSlide) dot.classList.add('active');
      
      dot.addEventListener('click', () => {
        if (isAnimating || index === currentSlide) return;
        goToSlide(index);
      });
      
      dotsContainer.appendChild(dot);
    });
  }

  // Cập nhật trạng thái active của dots
  function updateDots() {
    const dots = document.querySelectorAll('.dot');
    dots.forEach((dot, index) => {
      dot.classList.toggle('active', index === currentSlide);
    });
  }

  // Chuyển đến slide cụ thể
  function goToSlide(index) {
    if (isAnimating || index === currentSlide) return;
    isAnimating = true;

    // Xác định hướng chuyển
    const direction = determineDirection(index);

    // Chuẩn bị slide mới
    const newSlide = slides[index];
    const currentSlideElement = slides[currentSlide];
    
    // Xóa tất cả các class không cần thiết từ tất cả slide
    slides.forEach(slide => {
      if (slide !== newSlide && slide !== currentSlideElement) {
        slide.classList.remove('active', 'previous', 'next');
      }
    });

    if (direction === 'next') {
      // Chuẩn bị slide mới ở bên phải
      newSlide.classList.remove('previous');
      newSlide.classList.add('next');
      
      // Đảm bảo browser render
      setTimeout(() => {
        // Chuyển slide hiện tại sang trái và slide mới vào giữa
        currentSlideElement.classList.remove('active');
        currentSlideElement.classList.add('previous');
        
        newSlide.classList.remove('next');
        newSlide.classList.add('active');
        
        // Cập nhật biến currentSlide
        currentSlide = index;
        
        // Cập nhật dots
        updateDots();
        
        // Đặt thời gian chờ cho animation
        setTimeout(() => {
          isAnimating = false;
        }, 500);
      }, 50);
    } else {
      // Chuẩn bị slide mới ở bên trái
      newSlide.classList.remove('next');
      newSlide.classList.add('previous');
      
      // Đảm bảo browser render
      setTimeout(() => {
        // Chuyển slide hiện tại sang phải và slide mới vào giữa
        currentSlideElement.classList.remove('active');
        currentSlideElement.classList.add('next');
        
        newSlide.classList.remove('previous');
        newSlide.classList.add('active');
        
        // Cập nhật biến currentSlide
        currentSlide = index;
        
        // Cập nhật dots
        updateDots();
        
        // Đặt thời gian chờ cho animation
        setTimeout(() => {
          isAnimating = false;
        }, 500);
      }, 50);
    }
  }

  // Xác định hướng tối ưu để chuyển slide
  function determineDirection(targetIndex) {
    // Tính khoảng cách theo chiều thuận
    const forwardDistance = (targetIndex - currentSlide + totalSlides) % totalSlides;
    // Tính khoảng cách theo chiều ngược
    const backwardDistance = (currentSlide - targetIndex + totalSlides) % totalSlides;
    
    // Trả về hướng tối ưu
    return forwardDistance <= backwardDistance ? 'next' : 'prev';
  }

  // Chuyển đến slide tiếp theo
  function nextSlide() {
    if (isAnimating) return;
    const nextIndex = (currentSlide + 1) % totalSlides;
    goToSlide(nextIndex);
  }

  // Chuyển đến slide trước đó
  function prevSlide() {
    if (isAnimating) return;
    const prevIndex = (currentSlide - 1 + totalSlides) % totalSlides;
    goToSlide(prevIndex);
  }

  // Thiết lập các event listener
  nextButton.addEventListener('click', () => {
    nextSlide();
    resetInterval();
  });

  prevButton.addEventListener('click', () => {
    prevSlide();
    resetInterval();
  });

  // Tự động chuyển slide
  let slideInterval = setInterval(nextSlide, 5000);

  function resetInterval() {
    clearInterval(slideInterval);
    slideInterval = setInterval(nextSlide, 5000);
  }
});

