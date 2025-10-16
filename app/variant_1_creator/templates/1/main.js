  const track = document.getElementById('sliderTrack');
  const slides = track.querySelectorAll('img');
  const totalSlides = slides.length;
  let currentIndex = 0;

  function moveSlide(direction) {
    currentIndex += direction;

    if (currentIndex < 0) currentIndex = totalSlides - 1;
    if (currentIndex >= totalSlides) currentIndex = 0;

    const slideWidth = slides[0].clientWidth;
    track.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
  }

  window.addEventListener('resize', () => {
    moveSlide(0); // Recalculate position on resize
  });
const slider = document.querySelector('.slider-track');
const items = slider.querySelectorAll('img');
const dotsList = document.querySelector('.dots');
let active = 0;

// Create dots dynamically
items.forEach((item, key) => {
  const dot = document.createElement('li');
  dotsList.appendChild(dot);

  dot.addEventListener('click', () => {
    active = key;
    reloadSlider();
  });

  if (key === 0) {
    dot.classList.add('active');
  }
});

let dots = document.querySelectorAll('.slider-container .dots li');

// Update slider scroll position and active dot
function reloadSlider() {
  const width = slider.clientWidth;
  slider.scrollTo({
    left: width * active,
    behavior: 'smooth'
  });

  dots.forEach(dot => dot.classList.remove('active'));
  dots[active].classList.add('active');
}

// Optional: update dots on manual scroll/swipe
slider.addEventListener('scroll', () => {
  const index = Math.round(slider.scrollLeft / slider.clientWidth);
  if (index !== active) {
    active = index;
    dots.forEach(dot => dot.classList.remove('active'));
    if (dots[active]) dots[active].classList.add('active');
  }
});
