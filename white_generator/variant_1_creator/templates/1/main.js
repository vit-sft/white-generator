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

//For About Button
const about = document.querySelector('#about.description');
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

// Optional: adjust collapsedHeight if viewport resizes
window.addEventListener('resize', () => {
    if (about.classList.contains('collapsed')) {
    paragraph.style.maxHeight = window.innerHeight * 0.3 + 'px';
    }
});
}

//For carousel scrolling
const carousel = document.querySelector('.carousel__track');
let scrollAmount = 0;
let isScrolling = true; // flag to control auto scroll

// Auto scroll function
function autoScroll() {
  if (isScrolling) {
    scrollAmount += 2; // pixels per frame

    // Loop back to start
    if (scrollAmount >= carousel.scrollWidth - carousel.clientWidth) {
      scrollAmount = 0;
    }

    carousel.scrollLeft = scrollAmount;
  } else {
    // When user scrolls manually, sync scrollAmount to their scroll
    scrollAmount = carousel.scrollLeft;
  }

  requestAnimationFrame(autoScroll);
}

// Pause auto scroll on user interaction
carousel.addEventListener('mousedown', () => isScrolling = false);
carousel.addEventListener('touchstart', () => isScrolling = false);

// Resume auto scroll after user stops interacting
carousel.addEventListener('mouseup', () => isScrolling = true);
carousel.addEventListener('touchend', () => isScrolling = true);
carousel.addEventListener('mouseleave', () => isScrolling = true);

// Sync scrollAmount on manual scroll
carousel.addEventListener('scroll', () => {
  if (!isScrolling) {
    scrollAmount = carousel.scrollLeft;
  }
});

// Start auto scroll
autoScroll();

document.querySelector('.download_button').onclick = e => window.open(e.currentTarget.getAttribute('href'), '_blank');