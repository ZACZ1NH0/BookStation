document.addEventListener('DOMContentLoaded', function () {
  // Xử lý popup nếu có
  setupUserPopup();
  
  // Hiệu ứng đẹp cho các sách khi trang tải xong
  animateBookCardsOnLoad();
});

// Thiết lập user popup nếu có
function setupUserPopup() {
  const userIcon = document.getElementById('user-icon');
  const userPopup = document.getElementById('user-popup');

  if (userIcon && userPopup) {
    userIcon.addEventListener('click', function (e) {
      e.stopPropagation();
      if (userPopup.style.display === 'block') {
        userPopup.style.display = 'none';
      } else {
        userPopup.style.display = 'block';
      }
    });

    document.addEventListener('click', function () {
      if (userPopup.style.display === 'block') {
        userPopup.style.display = 'none';
      }
    });

    userPopup.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }
}

// Hiệu ứng xuất hiện dần dần cho các card sách
function animateBookCardsOnLoad() {
  const books = document.querySelectorAll('.book');
  books.forEach((book, index) => {
    book.style.opacity = '0';
    book.style.transform = 'translateY(20px)';
    
    setTimeout(() => {
      book.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
      book.style.opacity = '1';
      book.style.transform = 'translateY(0)';
    }, 100 + (index * 50));
  });
}

// Hàm giảm số lượng - được gọi trực tiếp từ onclick
function decreaseQuantity(button) {
  const input = button.nextElementSibling;
  let value = parseInt(input.value);
  if (value > 1) {
    value--;
    input.value = value;
    animateQuantityChange(input, 'decrease');
    animateButton(button);
  }
}

// Hàm tăng số lượng - được gọi trực tiếp từ onclick
function increaseQuantity(button) {
  const input = button.previousElementSibling;
  let value = parseInt(input.value);
  value++;
  input.value = value;
  animateQuantityChange(input, 'increase');
  animateButton(button);
}

// Hiệu ứng khi thay đổi số lượng
function animateQuantityChange(input, direction) {
  input.classList.add('pulse');
  
  // Hiệu ứng tăng/giảm
  if (direction === 'increase') {
    input.classList.add('increase');
  } else {
    input.classList.add('decrease');
  }
  
  // Xóa class sau khi hiệu ứng hoàn thành
  setTimeout(() => {
    input.classList.remove('pulse', 'increase', 'decrease');
  }, 300);
}

// Hiệu ứng nhấn nút
function animateButton(button) {
  button.style.transform = 'scale(0.95)';
  setTimeout(() => {
    button.style.transform = 'scale(1)';
  }, 100);
}
