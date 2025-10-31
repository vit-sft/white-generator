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