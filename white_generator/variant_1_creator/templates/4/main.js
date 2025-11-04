const acc = document.querySelectorAll(".footer-accordion h3");
acc.forEach((header) => {
    header.addEventListener("click", () => {
        const content = header.nextElementSibling;
        if(content.style.display === "block") {
            content.style.display = "none";
        } else {
            // close others
            document.querySelectorAll(".footer-accordion .content").forEach((c) => c.style.display = "none");
            content.style.display = "block";
        }
    });
});


// For About Button
const about = document.querySelector(".about-container");
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
        const lastChild = about.lastElementChild;
        about.insertBefore(more, lastChild);

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


const screenshots = Array.from(document.querySelectorAll('.carousel__track img')).map(img => img.src);

const currentImg = document.querySelector('.phone-content.current');
const nextImg = document.querySelector('.phone-content.next');

let index = 0;

setInterval(() => {
  const nextIndex = (index + 1) % screenshots.length;

  // Prepare the next image behind the current one
  nextImg.src = screenshots[nextIndex];
  nextImg.style.transition = "none";
  nextImg.style.opacity = 0;

  // Force reflow so browser registers the reset before animating
  void nextImg.offsetWidth;

  // Start the fade transition
  nextImg.style.transition = "opacity 0.6s ease-in-out";
  nextImg.style.opacity = 1;
  currentImg.style.opacity = 0;

  // After transition, swap roles
  setTimeout(() => {
    currentImg.src = screenshots[nextIndex];
    currentImg.style.opacity = 1;
    nextImg.style.opacity = 0;

    index = nextIndex;
  }, 200); // match transition time
}, 2000);