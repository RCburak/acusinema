document.addEventListener('DOMContentLoaded', () => {
    // DOM elementlerini seç
    const track = document.querySelector('.slider-track-js');
    const slides = document.querySelectorAll('.slide-js');
    const prevButton = document.querySelector('.prev-button');
    const nextButton = document.querySelector('.next-button');

    const totalSlides = slides.length;
    let currentSlideIndex = 0;
    
    // Geçiş süresi: 3000 milisaniye = 3 saniye
    const transitionTime = 3000;
    let autoSlideInterval;

    // Slaytı kaydırma pozisyonuna ayarlar
    function updateSlidePosition() {
        // Kaydırma miktarı = - (Mevcut slayt indeksi * %100)
        const offset = currentSlideIndex * -100;
        track.style.transform = `translateX(${offset}%)`;
    }

    // Bir sonraki slayta geçer (Otomatik veya Buton ile)
    function nextSlide() {
        currentSlideIndex = (currentSlideIndex + 1) % totalSlides;
        updateSlidePosition();
    }

    // Bir önceki slayta geçer (Buton ile)
    function prevSlide() {
        currentSlideIndex = (currentSlideIndex - 1 + totalSlides) % totalSlides;
        updateSlidePosition();
    }
    
    // Otomatik kaydırmayı başlatır
    function startAutoSlide() {
        // Önceki intervali temizle ki çakışma olmasın
        clearInterval(autoSlideInterval); 
        autoSlideInterval = setInterval(nextSlide, transitionTime);
    }
    
    // Otomatik kaydırmayı durdurur
    function stopAutoSlide() {
        clearInterval(autoSlideInterval);
    }

    // Butonlara event listener ekle
    nextButton.addEventListener('click', () => {
        stopAutoSlide(); // Butona basılınca otomatik geçişi durdur
        nextSlide();
        startAutoSlide(); // Tekrar başlat
    });

    prevButton.addEventListener('click', () => {
        stopAutoSlide(); // Butona basılınca otomatik geçişi durdur
        prevSlide();
        startAutoSlide(); // Tekrar başlat
    });

    // KRİTİK DÜZELTME: Sayfa yüklendiğinde slaytı 0. pozisyonda sabitler.
    updateSlidePosition();

    // Başlangıçta otomatik kaydırmayı başlat
    if (totalSlides > 1) {
        startAutoSlide();
    }
});