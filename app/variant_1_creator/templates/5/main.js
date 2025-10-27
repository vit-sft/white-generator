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
