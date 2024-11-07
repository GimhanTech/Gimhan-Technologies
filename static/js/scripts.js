// Dynamic Fade-In for Scroll
document.addEventListener('scroll', function() {
    const elements = document.querySelectorAll('.fade-in, .slide-up');
    const scrollPosition = window.scrollY + window.innerHeight;

    elements.forEach(element => {
        if (element.getBoundingClientRect().top + window.scrollY < scrollPosition) {
            element.style.opacity = 1;
            element.style.transform = 'translateY(0)';
        }
    });
});

// Smooth Scroll for Navigation Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("backgroundRemoverForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    form.addEventListener("submit", function() {
        // Show loading overlay when the form is submitted
        loadingOverlay.style.display = "flex";
    });
});
document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("grammarAnalyzerForm");
    const loadingOverlay = document.getElementById("loadingOverlay");

    form.addEventListener("submit", function() {
        // Show loading overlay when the form is submitted
        loadingOverlay.style.display = "flex";
    });
});

