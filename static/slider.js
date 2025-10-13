document.addEventListener('DOMContentLoaded', () => {
    const track = document.querySelector('.slider-track-js');
    if (!track) return;

    const slides = Array.from(track.children);
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    if (!prevButton || !nextButton || slides.length === 0) {
        if (prevButton) prevButton.style.display = 'none';
        if (nextButton) nextButton.style.display = 'none';
        return;
    }

    const totalSlides = slides.length;
    let currentSlideIndex = 0;
    const transitionTime = 4000;
    let autoSlideInterval;

    // track'in genişliğini slayt sayısına göre ayarla (Örn: 3 slayt için %300)
    track.style.width = `${totalSlides * 100}%`;

    // Her bir slaytın, track içindeki genişliğini ayarla (Örn: 3 slayt varsa her biri %33.33)
    slides.forEach(slide => {
        slide.style.width = `${100 / totalSlides}%`;
    });
    
    function updateSlidePosition() {
        const offset = currentSlideIndex * (100 / totalSlides);
        track.style.transform = `translateX(-${offset}%)`;
    }

    function nextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
        updateSlidePosition();
    }

    function prevSlide() {
        currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
        updateSlidePosition();
    }
    
    function startAutoSlide() {
        clearInterval(autoSlideInterval); 
        autoSlideInterval = setInterval(nextSlide, transitionTime);
    }
    
    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    nextButton.addEventListener('click', () => {
        stopAutoSlide();
        nextSlide();
        startAutoSlide();
    });

    prevButton.addEventListener('click', () => {
        stopAutoSlide();
        prevSlide();
        startAutoSlide();
    });

    updateSlidePosition();

    if (totalSlides > 1) {
        startAutoSlide();
    }
});