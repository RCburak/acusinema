# core/views.py

from django.shortcuts import render # pyright: ignore[reportMissingModuleSource]

def anasayfa(request):
    context = {
        'baslik': 'AcuSinema Kulübü',
        'karsilama_metni': 'Sinema tutkunlarının buluşma noktası.'
    }
    
    # anasayfa.html şablonunu doğrudan templates klasöründen çağırıyoruz
    return render(request, 'anasayfa.html', context)

# YENİ EKLENEN FONKSİYON
def iletisim_sayfasi(request):
    # Bu view, herhangi bir context göndermeden doğrudan iletisim.html'yi gösterecek
    return render(request, 'iletisim.html')