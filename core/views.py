# core/views.py

from django.shortcuts import render

def anasayfa(request):
    context = {
        'baslik': 'AcuSinema Kulübü',
        'karsilama_metni': 'Sinema tutkunlarının buluşma noktası.'
    }
    return render(request, 'anasayfa.html', context)

def iletisim_sayfasi(request):
    return render(request, 'iletisim.html')

def filmler_sayfasi(request):
    context = {} 
    return render(request, 'filmler.html', context)

def etkinlikler_sayfasi(request):
    context = {}
    return render(request, 'etkinlikler.html', context)