const acc = document.querySelectorAll(".footer-accordion h3");
acc.forEach((header) => {
  header.addEventListener("click", () => {
    const content = header.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      // close others
      document
        .querySelectorAll(".footer-accordion .content")
        .forEach((c) => (c.style.display = "none"));
      content.style.display = "block";
    }
  });
});

// For About Button
const about = document.querySelector(".description-block");
if (about) {
  const paragraph = about.querySelector("p");

  function setAboutHeight() {
    // Use 70% for desktop, 40% for mobile
    const collapsedHeight =
      window.innerWidth <= 768
        ? window.innerHeight * 0.4
        : window.innerHeight * 0.7;

    if (paragraph.scrollHeight > collapsedHeight) {
      about.classList.add("collapsed");
      paragraph.style.maxHeight = collapsedHeight + "px";

      // Create or reuse "Read More" button
      let more = about.querySelector(".read-more");
      if (!more) {
        more = document.createElement("span");
        more.textContent = "Read More";
        more.className = "read-more";
        about.appendChild(more);

        more.addEventListener("click", () => {
          if (about.classList.contains("collapsed")) {
            // Expand
            paragraph.style.maxHeight = paragraph.scrollHeight + "px";
            about.classList.remove("collapsed");
            more.textContent = "Read Less";
          } else {
            // Collapse
            paragraph.style.maxHeight = collapsedHeight + "px";
            about.classList.add("collapsed");
            more.textContent = "Read More";
          }
        });
      } else if (about.classList.contains("collapsed")) {
        paragraph.style.maxHeight = collapsedHeight + "px";
      }
    } else {
      // If paragraph fits, remove collapse state and button
      about.classList.remove("collapsed");
      paragraph.style.maxHeight = "none";
      const btn = about.querySelector(".read-more");
      if (btn) btn.remove();
    }
  }

  // Initial setup
  setAboutHeight();

  // Update on window resize
  window.addEventListener("resize", setAboutHeight);
}

// Fotorama's code with gallery
const slides = document.querySelectorAll(".gallery-container > div");
const thumbs = document.querySelectorAll(".thumbnails > div");
const gallery = document.querySelector(".gallery-section");
let current = 0;
let interval;

slides[current].classList.add("active");
thumbs[current].classList.add("active");

function showSlide(index) {
  slides[current].classList.remove("active");
  thumbs[current].classList.remove("active");
  current = index;
  slides[current].classList.add("active");
  thumbs[current].classList.add("active");
}

function nextSlide() {
  showSlide((current + 1) % slides.length);
}

function startSlideshow() {
  interval = setInterval(nextSlide, 2000);
}

function stopSlideshow() {
  clearInterval(interval);
}

startSlideshow();

// Pause/resume on hover
gallery.addEventListener("mouseenter", stopSlideshow);
gallery.addEventListener("mouseleave", startSlideshow);

// Click thumbnails
thumbs.forEach((thumb, index) => {
  thumb.addEventListener("click", () => {
    stopSlideshow();
    showSlide(index);
  });
});

document.querySelector('div .hero-button').onclick = e => window.open(e.currentTarget.getAttribute('href'), '_blank');
document.querySelector('div .download-button').onclick = e => window.open(e.currentTarget.getAttribute('href'), '_blank');

document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', e => {
        e.preventDefault();

        const targetId = link.getAttribute('href').substring(1);
        const targetElement = document.getElementById(targetId);

        if (targetElement) {
            targetElement.scrollIntoView({ behavior: 'smooth' });
        }
    });
});