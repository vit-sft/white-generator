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