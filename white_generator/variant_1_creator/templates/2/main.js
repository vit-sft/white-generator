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
function moveFooterForMobile() {
    const footer = document.querySelector("footer");
    const body = document.body;

    if (window.innerWidth <= 768) {
        // Move footer to end of body
        if (!body.contains(footer) || footer.parentElement !== body) {
            body.appendChild(footer);
        }
    } else {
        // Move footer back to original sidebar
        const sidebar = document.querySelector(".sidebar");
        if (sidebar && sidebar.contains(footer) === false) {
            sidebar.appendChild(footer);
        }
    }
}

// Initial check
moveFooterForMobile();

// Update on resize
window.addEventListener("resize", moveFooterForMobile);


//For About Button
const about = document.querySelector('.sidebar .description');
const paragraph = about.querySelector('p');
const collapsedHeight = window.innerHeight * 0.3; // 30dvh in px

// Only show "Read More" if paragraph is taller than collapsed height
if (paragraph.scrollHeight > collapsedHeight) {
about.classList.add('collapsed');
paragraph.style.maxHeight = collapsedHeight + 'px';

const more = document.createElement('span');
more.textContent = 'Read More';
more.className = 'read-more';
about.appendChild(more);

more.addEventListener('click', () => {
    if (about.classList.contains('collapsed')) {
    // expand
    paragraph.style.maxHeight = paragraph.scrollHeight + 'px';
    about.classList.remove('collapsed');
    more.textContent = 'Read Less';
    } else {
    // collapse
    paragraph.style.maxHeight = collapsedHeight + 'px';
    about.classList.add('collapsed');
    more.textContent = 'Read More';
    }
});

}

// For carousel scrolling
const carousel = document.querySelector(".main-content");
let scrollAmount = 0;
let isScrolling = true;

function autoScroll() {
  if (!carousel) return;

  const isMobile = window.innerWidth <= 768; // Detect screen size

  if (isScrolling) {
    scrollAmount += 2; // pixels per frame

    if (isMobile) {
      // Horizontal scroll on mobile
      if (scrollAmount >= carousel.scrollWidth - carousel.clientWidth) {
        scrollAmount = 0;
      }
      carousel.scrollLeft = scrollAmount;
    } else {
      // Vertical scroll on desktop
      if (scrollAmount >= carousel.scrollHeight - carousel.clientHeight) {
        scrollAmount = 0;
      }
      carousel.scrollTop = scrollAmount;
    }
  } else {
    // Sync manual scroll
    scrollAmount = isMobile ? carousel.scrollLeft : carousel.scrollTop;
  }

  requestAnimationFrame(autoScroll);
}

// Pause/resume on user interaction
carousel.addEventListener("mousedown", () => (isScrolling = false));
carousel.addEventListener("touchstart", () => (isScrolling = false));
carousel.addEventListener("mouseup", () => (isScrolling = true));
carousel.addEventListener("touchend", () => (isScrolling = true));
carousel.addEventListener("mouseleave", () => (isScrolling = true));

// Sync on scroll
carousel.addEventListener("scroll", () => {
  if (!isScrolling) {
    scrollAmount =
      window.innerWidth <= 768 ? carousel.scrollLeft : carousel.scrollTop;
  }
});

// Start auto scroll
autoScroll();

document.querySelector('.download_button').onclick = e => window.open(e.currentTarget.getAttribute('href'), '_blank');