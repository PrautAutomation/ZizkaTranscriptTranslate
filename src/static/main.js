/* Moved the inline JavaScript to this file so it can keep the html cleaner */
/* script */
const recorder = document.getElementById('recorder');
const player = document.getElementById('player');

recorder.addEventListener('change', function (e) {
  const file = e.target.files[0];
  const url = URL.createObjectURL(file);
  player.src = url;
});
/* /script */

/* Logo animation script - maximálně kompatibilní řešení pro všechny prohlížeče */
document.addEventListener('DOMContentLoaded', function() {
  try {
    // Cesty k obrázkům
    var logoImages = [
      '../static/img/VojtaLogo00.png', // Základní obrázek
      '../static/img/VojtaLogo01.png',
      '../static/img/VojtaLogo02.png',
      '../static/img/VojtaLogo03.png',
      '../static/img/VojtaLogo04.png',
      '../static/img/VojtaLogo05.png',
      '../static/img/VojtaLogo06.png',
      '../static/img/VojtaLogo07.png'
    ];
    
    // Reference na elementy - používáme getElementById, který je podporován všude
    var baseImage = document.getElementById('baseImage');
    var overlayImage = document.getElementById('overlayImage');
    
    // Proměnné pro animaci
    var currentImageIndex = 0;
    var animationInProgress = false;
    var fadeInterval = null;
    var currentOpacity = 0;
    
    // Funkce pro získání náhodného indexu (kromě aktuálního a základního)
    function getRandomImageIndex() {
      // Vybíráme pouze z indexů 1-7 (ne základní obrázek)
      var min = 1;
      var max = logoImages.length - 1;
      
      if (max <= min) return min;
      
      var newIndex;
      do {
        newIndex = Math.floor(Math.random() * (max - min + 1)) + min;
      } while (newIndex === currentImageIndex);
      
      return newIndex;
    }
    
    // Funkce pro nastavení opacity - kompatibilní se všemi prohlížeči
    function setOpacity(element, opacity) {
      if (!element) return;
      
      // Nastavení opacity pro všechny prohlížeče
      element.style.opacity = opacity;
      element.style.filter = 'alpha(opacity=' + (opacity * 100) + ')'; // Pro IE8 a starší
      element.style.MozOpacity = opacity; // Pro starší Firefox
      element.style.KhtmlOpacity = opacity; // Pro starší Safari
    }
    
    // Funkce pro postupné zvýšení opacity (fade in)
    function fadeIn() {
      if (currentOpacity >= 1) {
        clearInterval(fadeInterval);
        // Po dokončení fade in počkat 2 sekundy a pak spustit fade out
        setTimeout(fadeOut, 2000);
        return;
      }
      
      currentOpacity += 0.05;
      setOpacity(overlayImage, currentOpacity);
    }
    
    // Funkce pro postupné snížení opacity (fade out)
    function fadeOut() {
      clearInterval(fadeInterval);
      
      fadeInterval = setInterval(function() {
        if (currentOpacity <= 0) {
          clearInterval(fadeInterval);
          // Po dokončení fade out počkat 1 sekundu a resetovat stav
          setTimeout(function() {
            animationInProgress = false;
          }, 1000);
          return;
        }
        
        currentOpacity -= 0.05;
        setOpacity(overlayImage, currentOpacity);
      }, 50);
    }
    
    // Funkce pro spuštění animace
    function startTransition() {
      if (animationInProgress) return;
      animationInProgress = true;
      
      try {
        // Vybrat náhodný obrázek
        var logoIndex = getRandomImageIndex();
        currentImageIndex = logoIndex;
        
        // Nastavit nový obrázek
        overlayImage.src = logoImages[logoIndex];
        
        // Resetovat opacity
        currentOpacity = 0;
        setOpacity(overlayImage, 0);
        
        // Spustit fade in
        clearInterval(fadeInterval);
        fadeInterval = setInterval(fadeIn, 50);
      } catch (e) {
        console.error('Chyba při animaci:', e);
        animationInProgress = false;
      }
    }
    
    // Spustit animaci každých 5 sekund
    setTimeout(function() {
      try {
        startTransition();
        setInterval(startTransition, 5000);
      } catch (e) {
        console.error('Chyba při spuštění animace:', e);
      }
    }, 1000); // Počkat 1 sekundu po načtení stránky před spuštěním první animace
  } catch (e) {
    console.error('Chyba při inicializaci animace:', e);
  }
});

/* script */
const conversionForm = document.getElementById('conversion-form');
const submitButton = document.getElementById('submit');
const spinner = document.getElementById('spinner');

conversionForm.addEventListener('submit', async (event) => {
event.preventDefault();
submitButton.disabled = true;
spinner.classList.remove('d-none');

const formData = new FormData(conversionForm);
const response = await fetch('/download/', {
    method: 'POST',
    body: formData,
});

const blob = await response.blob();
const downloadUrl = URL.createObjectURL(blob);
const link = document.createElement('a');
link.href = downloadUrl;
link.download = `${formData.get('filename')}.${formData.get('file_type')}`;
document.body.appendChild(link);
link.click();
document.body.removeChild(link);
submitButton.disabled = false;
spinner.classList.add('d-none');
});
/* /script */
