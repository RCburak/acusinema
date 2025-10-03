# core/views.py

from django.shortcuts import render

def anasayfa(request):
    context = {
        'baslik': 'AcuSinema Kulübü',
        'karsilama_metni': 'Sinema tutkunlarının buluşma noktası.'
    }
    
    # anasayfa.html şablonunu doğrudan templates klasöründen çağırıyoruz
    return render(request, 'anasayfa.html', context)