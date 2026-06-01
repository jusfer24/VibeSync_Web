/* =========================================================
   VIBESYNC main.js v2.0
   Player controls, toasts, ripples, sidebar, particles
   ========================================================= */

document.addEventListener('DOMContentLoaded', () => {

  /* ── 1. SIDEBAR TOGGLE ──────────────────────────── */
  const menuToggle = document.getElementById('menuToggle');
  const sidebar    = document.getElementById('sidebar');

  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      if (window.innerWidth <= 768) {
        sidebar.classList.toggle('mobile-active');
      } else {
        sidebar.classList.toggle('hidden');
        localStorage.setItem('vibeSyncMenu',
          sidebar.classList.contains('hidden') ? 'hidden' : 'expanded');
      }
    });
    // Restore saved state
    if (localStorage.getItem('vibeSyncMenu') === 'hidden' && window.innerWidth > 768) {
      sidebar.classList.add('hidden');
    }
  }

  /* ── 2. PAGE ENTRANCE ANIMATION ─────────────────── */
  const mainContent = document.querySelector('.main-content');
  if (mainContent) {
    mainContent.style.animation = 'fade-up 0.45s cubic-bezier(0,0,0.2,1) both';
  }

  /* ── 3. RIPPLE EFFECT on buttons ─────────────────── */
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn, button, .music-card, .ticket-card');
    if (!btn || btn.classList.contains('no-ripple')) return;
    const rect   = btn.getBoundingClientRect();
    const circle = document.createElement('span');
    const size   = Math.max(rect.width, rect.height) * 2;
    circle.style.cssText = `
      width: ${size}px; height: ${size}px;
      left: ${e.clientX - rect.left - size/2}px;
      top:  ${e.clientY - rect.top  - size/2}px;
      position: absolute; border-radius: 50%;
      background: rgba(255,255,255,0.18);
      transform: scale(0); animation: ripple 0.55s linear;
      pointer-events: none;
    `;
    const prevPos = getComputedStyle(btn).position;
    if (prevPos === 'static') btn.style.position = 'relative';
    btn.style.overflow = 'hidden';
    btn.appendChild(circle);
    circle.addEventListener('animationend', () => circle.remove());
  });

  /* ── 4. TOAST SYSTEM ─────────────────────────────── */
  window.vibeToast = (msg, type = 'info', duration = 3500) => {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const icons = { info: '🎵', success: '✅', error: '❌', warning: '⚠️' };
    const toast = document.createElement('div');
    toast.className = `toast-msg ${type}`;
    toast.innerHTML = `<span>${icons[type] || '🎵'}</span><span>${msg}</span>`;
    container.appendChild(toast);
    setTimeout(() => {
      toast.style.animation = 'none';
      toast.style.transition = 'opacity 0.3s, transform 0.3s';
      toast.style.opacity = '0';
      toast.style.transform = 'translateX(30px)';
      setTimeout(() => toast.remove(), 350);
    }, duration);
  };

  /* ── 5. MINI PLAYER ──────────────────────────────── */
  const playerState = {
    playing: false,
    progress: 32,
    volume: 75,
    liked: false,
    tracks: [
      { name: 'Pichincha Nightfall', artist: 'MatS', color: 'f5a623' },
      { name: 'Amanecer Neón', artist: 'DJ Santi', color: '00e5ff' },
      { name: 'Crimen Perfecto', artist: 'Guardarraya', color: '8e44ad' },
      { name: '1537', artist: 'Guardarraya', color: '50e3c2' },
    ],
    currentTrack: 0,
  };

  const player = document.querySelector('.mini-player');
  if (player) {
    const playBtn      = player.querySelector('.play-pause');
    const progressFill = player.querySelector('.progress-fill');
    const progressTrack= player.querySelector('.progress-track');
    const volFill      = player.querySelector('.vol-fill');
    const volTrack     = player.querySelector('.vol-bar');
    const waveform     = player.querySelector('.waveform');
    const likeBtn      = player.querySelector('.player-like-btn');
    const trackName    = player.querySelector('.player-track-name');
    const trackArtist  = player.querySelector('.player-track-artist');
    const thumb        = player.querySelector('.player-thumb');
    const currentTime  = player.querySelector('.time-current');
    const totalTime    = player.querySelector('.time-total');

    // Render track
    const renderTrack = () => {
      const t = playerState.tracks[playerState.currentTrack];
      if (trackName) trackName.textContent = t.name;
      if (trackArtist) trackArtist.textContent = t.artist;
      if (thumb) thumb.src = `https://placehold.co/52x52/${t.color}/0d1422?text=${t.name[0]}`;
    };
    renderTrack();

    // Play/Pause
    const togglePlay = () => {
      playerState.playing = !playerState.playing;
      if (playBtn) {
        playBtn.innerHTML = playerState.playing
          ? `<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg>`
          : `<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/></svg>`;
      }
      if (waveform) waveform.classList.toggle('playing', playerState.playing);
      if (thumb) thumb.classList.toggle('playing', playerState.playing);
    };
    if (playBtn) playBtn.addEventListener('click', togglePlay);

    // Progress bar simulate
    if (progressFill) progressFill.style.width = `${playerState.progress}%`;
    if (progressTrack) {
      progressTrack.addEventListener('click', (e) => {
        const rect = progressTrack.getBoundingClientRect();
        playerState.progress = ((e.clientX - rect.left) / rect.width) * 100;
        progressFill.style.width = `${playerState.progress}%`;
        const secs = Math.round(playerState.progress * 2.25);
        if (currentTime) currentTime.textContent = `${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;
      });
    }

    // Volume
    if (volFill) volFill.style.width = `${playerState.volume}%`;
    if (volTrack) {
      volTrack.addEventListener('click', (e) => {
        const rect = volTrack.getBoundingClientRect();
        playerState.volume = ((e.clientX - rect.left) / rect.width) * 100;
        volFill.style.width = `${playerState.volume}%`;
      });
    }

    // Like
    if (likeBtn) {
      likeBtn.addEventListener('click', () => {
        playerState.liked = !playerState.liked;
        likeBtn.classList.toggle('liked', playerState.liked);
        likeBtn.innerHTML = playerState.liked
          ? `<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>`
          : `<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 8 2.066 12.72-3.04 23.333 4.868 8 15z"/></svg>`;
        vibeToast(playerState.liked ? 'Añadido a Me gusta ❤️' : 'Quitado de Me gusta', playerState.liked ? 'success' : 'info');
      });
    }

    // Next / Prev
    const nextBtn = player.querySelector('.btn-next');
    const prevBtn = player.querySelector('.btn-prev');
    if (nextBtn) {
      nextBtn.addEventListener('click', () => {
        playerState.currentTrack = (playerState.currentTrack + 1) % playerState.tracks.length;
        renderTrack();
        vibeToast(`▶ ${playerState.tracks[playerState.currentTrack].name}`, 'info', 2000);
      });
    }
    if (prevBtn) {
      prevBtn.addEventListener('click', () => {
        playerState.currentTrack = (playerState.currentTrack - 1 + playerState.tracks.length) % playerState.tracks.length;
        renderTrack();
        vibeToast(`◀ ${playerState.tracks[playerState.currentTrack].name}`, 'info', 2000);
      });
    }

    // Simulate progress when playing
    let progressInterval;
    const startProgress = () => {
      progressInterval = setInterval(() => {
        if (!playerState.playing) return;
        playerState.progress = Math.min(playerState.progress + 0.05, 100);
        if (progressFill) progressFill.style.width = `${playerState.progress}%`;
        const secs = Math.round(playerState.progress * 2.25);
        if (currentTime) currentTime.textContent = `${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;
        if (playerState.progress >= 100) {
          playerState.currentTrack = (playerState.currentTrack + 1) % playerState.tracks.length;
          playerState.progress = 0;
          renderTrack();
        }
      }, 300);
    };
    startProgress();

    // Space bar toggle play
    document.addEventListener('keydown', (e) => {
      if (e.code === 'Space' && !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
        e.preventDefault();
        togglePlay();
      }
    });
  }

  /* ── 6. HOVER 3D TILT on Music Cards ─────────────── */
  document.querySelectorAll('.music-card .img-wrapper').forEach(card => {
    card.addEventListener('mousemove', (e) => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left - rect.width / 2)  / (rect.width  / 2);
      const y = (e.clientY - rect.top  - rect.height / 2) / (rect.height / 2);
      card.style.transform = `perspective(400px) rotateY(${x * 8}deg) rotateX(${-y * 8}deg) scale(1.04)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
      card.style.transition = 'transform 0.4s ease';
    });
  });

  /* ── 7. ANIMATED NUMBER COUNT-UP ─────────────────── */
  const countUp = (el) => {
    const target = parseFloat(el.dataset.count || el.textContent.replace(/[^0-9.]/g, ''));
    if (isNaN(target)) return;
    const suffix = el.textContent.replace(/[0-9.,]/g, '');
    const duration = 1500;
    const start = performance.now();
    const step = (now) => {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      const value = Math.floor(eased * target);
      el.textContent = value.toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };

  // Intersect observe stat values
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        countUp(e.target);
        observer.unobserve(e.target);
      }
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.stat-value[data-count]').forEach(el => observer.observe(el));

  /* ── 8. SMOOTH SCROLL ROW (drag to scroll) ────────── */
  document.querySelectorAll('.scroll-row').forEach(row => {
    let isDown = false, startX, scrollLeft;
    row.addEventListener('mousedown',  e => { isDown = true; startX = e.pageX - row.offsetLeft; scrollLeft = row.scrollLeft; row.style.cursor = 'grabbing'; });
    row.addEventListener('mouseleave', () => { isDown = false; row.style.cursor = ''; });
    row.addEventListener('mouseup',    () => { isDown = false; row.style.cursor = ''; });
    row.addEventListener('mousemove',  e => {
      if (!isDown) return;
      e.preventDefault();
      const x = e.pageX - row.offsetLeft;
      row.scrollLeft = scrollLeft - (x - startX) * 1.5;
    });
  });

  /* ── 9. PROGRESS BAR ANIMATION ───────────────────── */
  document.querySelectorAll('.progress-bar').forEach(bar => {
    const width = bar.style.width;
    bar.style.width = '0';
    setTimeout(() => { bar.style.width = width; }, 300);
  });

  /* ── 10. GENRE BADGE HOVER GLOW ──────────────────── */
  document.querySelectorAll('.badge').forEach(badge => {
    badge.addEventListener('mouseenter', () => {
      badge.style.transform = 'scale(1.08)';
      badge.style.transition = 'transform 0.2s';
    });
    badge.addEventListener('mouseleave', () => {
      badge.style.transform = '';
    });
  });

  /* ── 11. FORM VALIDATION FEEDBACK ────────────────── */
  document.querySelectorAll('form input[required], form select[required]').forEach(input => {
    input.addEventListener('invalid', () => {
      input.style.borderColor = 'var(--rose)';
      input.style.boxShadow = '0 0 0 3px rgba(251,113,133,0.15)';
    });
    input.addEventListener('input', () => {
      input.style.borderColor = '';
      input.style.boxShadow = '';
    });
  });

  /* ── 12. TABLE ROW STAGGER ───────────────────────── */
  document.querySelectorAll('.track-table tbody tr, .table tbody tr').forEach((row, i) => {
    row.style.animation = `fade-up 0.4s cubic-bezier(0,0,0.2,1) ${i * 0.04}s both`;
  });

  /* ── 13. NAV LINK ACTIVE HIGHLIGHT ──────────────── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link-custom').forEach(link => {
    if (link.href && link.href.includes(currentPath) && currentPath !== '/') {
      link.classList.add('active');
    }
  });

  /* ── 14. MOBILE SIDEBAR CLOSE ON OUTSIDE CLICK ──── */
  document.addEventListener('click', (e) => {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    if (window.innerWidth <= 768 && sidebar.classList.contains('mobile-active')) {
      if (!sidebar.contains(e.target) && !e.target.closest('#menuToggle')) {
        sidebar.classList.remove('mobile-active');
      }
    }
  });

  /* ── 15. COVER PREVIEW on upload ─────────────────── */
  document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
    input.addEventListener('change', () => {
      const file = input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (e) => {
        const zone = input.closest('.upload-cover-zone');
        if (!zone) return;
        zone.style.backgroundImage   = `url(${e.target.result})`;
        zone.style.backgroundSize    = 'cover';
        zone.style.backgroundPosition= 'center';
        zone.querySelectorAll('svg, span').forEach(el => el.style.opacity = '0');
        vibeToast('Portada cargada 🎨', 'success', 2000);
      };
      reader.readAsDataURL(file);
    });
  });

  /* ── 16. INITIAL TOAST ───────────────────────────── */
  const pageTitle = document.title.replace('VibeSync - ', '');
  if (pageTitle && pageTitle !== 'VibeSync') {
    setTimeout(() => vibeToast(`Bienvenido a ${pageTitle} 🎵`, 'info', 2500), 800);
  }

});