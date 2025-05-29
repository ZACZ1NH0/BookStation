document.addEventListener('DOMContentLoaded', function () {
  const userIcon = document.getElementById('user-icon');
  const userPopup = document.getElementById('user-popup');

  if (userIcon && userPopup) {
    userIcon.addEventListener('click', function (e) {
      e.stopPropagation(); // tránh nổi bọt sự kiện
      if (userPopup.style.display === 'block') {
        userPopup.style.display = 'none';
      } else {
        userPopup.style.display = 'block';
      }
    });

    // Click ra ngoài popup sẽ tắt popup
    document.addEventListener('click', function () {
      if (userPopup.style.display === 'block') {
        userPopup.style.display = 'none';
      }
    });

    // Ngăn popup đóng khi click bên trong popup
    userPopup.addEventListener('click', function (e) {
      e.stopPropagation();
    });
  }
});
