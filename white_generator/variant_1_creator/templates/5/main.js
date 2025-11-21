const acc = document.querySelectorAll(".footer-accordion h3");

acc.forEach((header) => {
  header.addEventListener("click", () => {
    const content = header.nextElementSibling;
    const parentAccordion = header.parentElement;

    if (content.style.display === "block") {
      // Close the current accordion
      content.style.display = "none";
      parentAccordion.style.flex = "1"; // shrink back
    } else {
      // Close others
      document.querySelectorAll(".footer-accordion").forEach((accordion) => {
        accordion.querySelector(".content").style.display = "none";
        accordion.style.flex = "1"; // reset flex
      });

      // Open current accordion
      content.style.display = "block";
      parentAccordion.style.flex = "2"; // expand
    }
  });
});

// For About Button
const about = document.querySelector("#about .container");
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

// For gallery
const gallery = document.querySelector(".gallery");
const allItems = Array.from(gallery.children);
const count = allItems.length;

// If only 0 or 1 image, just leave it static
if (count < 2) {
  gallery.style.display = "flex";
  gallery.style.justifyContent = "center";
  gallery.style.flexWrap = "wrap";
} else {
  // Choose number of rows dynamically
  let rows = 1;
  if (count > 8) rows = 2;
  if (count > 16) rows = 3;

  const perRow = Math.ceil(count / rows);

  // Reset gallery
  gallery.innerHTML = "";

  for (let r = 0; r < rows; r++) {
    const rowDiv = document.createElement("div");
    rowDiv.classList.add("scroll-row");

    const slice = allItems.slice(r * perRow, (r + 1) * perRow);

    // Duplicate images for seamless scroll
    const doubled = [...slice, ...slice];
    doubled.forEach((el) => rowDiv.appendChild(el.cloneNode(true)));

    // Alternate directions for variety
    if (r % 2 === 1) {
      rowDiv.style.animationDirection = "reverse";
    }

    gallery.appendChild(rowDiv);
  }

  gallery.style.gridTemplateRows = `repeat(${rows}, auto)`;
}
document.querySelector('div .download-btn').onclick = e => window.open(e.currentTarget.getAttribute('href'), '_blank');
