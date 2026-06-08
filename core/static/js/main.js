/* =========================================================
   VIBESYNC main.js v3.0
   Page loader · Scroll animations · Parallax · Player
   Toasts · Ripples · Drag-scroll · Skeleton · Transitions
   ========================================================= */

/* ── PAGE LOADER ── */
(function createLoader() {
  const loader = document.createElement('div');
  loader.id = 'vs-page-loader';
  loader.innerHTML = `
    <div class="loader-inner">
      <div class="loader-logo">🎵</div>
      <div class="loader-bars">
        <span></span><span></span><span></span><span></span><span></span>
      </div>
      <div class="loader-text">Cargando VibeSync…</div>
    </div>`;
  loader.style.cssText = `
    position:fixed;inset:0;z-index:99999;
    background:var(--bg-void,#03050c);
    display:flex;align-items:center;justify-content:center;
    flex-direction:column;
    transition:opacity .5s ease, transform .5s ease;
  `;
  const style = document.createElement('style');
  style.textContent = `
    .loader-inner{text-align:center;animation:scale-in .4s cubic-bezier(0.34,1.56,0.64,1)}
    .loader-logo{font-size:3rem;animation:float 2s ease-in-out infinite;margin-bottom:20px}
    .loader-bars{display:flex;align-items:flex-end;gap:5px;height:36px;justify-content:center;margin-bottom:16px}
    .loader-bars span{
      width:5px;border-radius:3px;
      background:linear-gradient(to top,#00e5ff,#a855f7);
      animation:wave-bar .7s ease-in-out infinite alternate;
    }
    .loader-bars span:nth-child(1){animation-delay:0s}
    .loader-bars span:nth-child(2){animation-delay:.12s}
    .loader-bars span:nth-child(3){animation-delay:.24s}
    .loader-bars span:nth-child(4){animation-delay:.36s}
    .loader-bars span:nth-child(5){animation-delay:.48s}
    .loader-text{font-size:.82rem;color:#5a6a8a;font-weight:600;letter-spacing:.1em;text-transform:uppercase;font-family:'Outfit',sans-serif}
    @keyframes wave-bar{from{height:6px}to{height:32px}}
    @keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
    @keyframes scale-in{from{opacity:0;transform:scale(.85)}to{opacity:1;transform:scale(1)}}
    @keyframes fade-up{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
    @keyframes ripple{to{transform:scale(3.5);opacity:0}}
    @keyframes gradient-drift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}
    @keyframes pulse-glow{0%,100%{box-shadow:0 0 10px rgba(0,229,255,.35)}50%{box-shadow:0 0 25px rgba(0,229,255,.6)}}
    @keyframes note-float{0%{opacity:0;transform:translateY(0) scale(.5)}20%{opacity:.7}80%{opacity:.3}100%{opacity:0;transform:translateY(-80px) rotate(15deg) scale(1)}}
    @keyframes rotate-disc{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    @keyframes slide-up-toast{from{transform:translateY(100%);opacity:0}to{transform:translateY(0);opacity:1}}
    @keyframes shimmer{0%{background-position:-200% 0}100%{background-position:200% 0}}
    @keyframes bounce-in{0%{transform:scale(0);opacity:0}60%{transform:scale(1.15)}80%{transform:scale(.95)}100%{transform:scale(1);opacity:1}}
    @keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}
    @keyframes particle-float{0%{opacity:0;transform:translateY(100vh)}10%{opacity:.6}90%{opacity:.3}100%{opacity:0;transform:translateY(-10vh)}}
  `;
  document.head.appendChild(style);
  document.body.appendChild(loader);
})();

/* ── HIDE LOADER on load ── */
window.addEventListener('load', () => {
  const loader = document.getElementById('vs-page-loader');
  if (!loader) return;
  setTimeout(() => {
    loader.style.opacity = '0';
    loader.style.transform = 'scale(1.04)';
    setTimeout(() => loader.remove(), 520);
  }, 600);
});

document.addEventListener('DOMContentLoaded', () => {

  /* ── SIDEBAR TOGGLE ── */
  const menuToggle = document.getElementById('menuToggle');
  const sidebar    = document.getElementById('sidebar');
  if (menuToggle && sidebar) {
    menuToggle.addEventListener('click', () => {
      if (window.innerWidth <= 768) sidebar.classList.toggle('mobile-active');
      else {
        sidebar.classList.toggle('hidden');
        localStorage.setItem('vibeSyncMenu', sidebar.classList.contains('hidden') ? 'hidden' : 'expanded');
      }
    });
    if (localStorage.getItem('vibeSyncMenu') === 'hidden' && window.innerWidth > 768)
      sidebar.classList.add('hidden');
  }

  /* ── SCROLL REVEAL (Intersection Observer) ── */
  const revealEls = document.querySelectorAll(
    '.stat-card, .premium-card, .ticket-card, .badge-card, .price-card, ' +
    '.music-card, .track-upload-row, .timeline-item, .faq-item, section, ' +
    '[data-reveal]'
  );

  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (!entry.isIntersecting) return;
      const el  = entry.target;
      const idx = Array.from(revealEls).indexOf(el);
      const delay = Math.min(idx * 30, 350);
      el.style.animation = `fade-up 0.55s cubic-bezier(0,0,0.2,1) ${delay}ms both`;
      revealObs.unobserve(el);
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => {
    el.style.opacity = '0';
    revealObs.observe(el);
  });

  /* ── STAGGER TABLE ROWS ── */
  document.querySelectorAll('.track-table tbody tr, #users-tbody tr').forEach((row, i) => {
    row.style.opacity = '0';
    setTimeout(() => {
      row.style.animation = `fade-up 0.4s cubic-bezier(0,0,0.2,1) ${i * 45}ms both`;
    }, 700);
  });

  /* ── COUNTER ANIMATION ── */
  const countObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target;
      const raw = el.dataset.count || el.textContent;
      const num = parseFloat(raw.replace(/[^0-9.]/g, ''));
      if (isNaN(num)) return;
      const suffix  = raw.replace(/[0-9.,]/g, '').trim();
      const prefix  = raw.match(/^[^0-9]*/)?.[0] || '';
      const dur = 1800;
      const start = performance.now();
      const step = (now) => {
        const p = Math.min((now - start) / dur, 1);
        const eased = 1 - Math.pow(1 - p, 4);
        const val   = Math.floor(eased * num);
        el.textContent = prefix + val.toLocaleString('es-EC') + suffix;
        if (p < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
      countObserver.unobserve(el);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-value[data-count], [data-counter]').forEach(el => countObserver.observe(el));

  /* ── RIPPLE on click ── */
  document.addEventListener('click', e => {
    const target = e.target.closest('button, .btn, .music-card, .ticket-card, .badge-card');
    if (!target || target.classList.contains('no-ripple')) return;
    const rect   = target.getBoundingClientRect();
    const circle = document.createElement('span');
    const size   = Math.max(rect.width, rect.height) * 2.2;
    circle.style.cssText = `
      width:${size}px;height:${size}px;
      left:${e.clientX - rect.left - size/2}px;
      top:${e.clientY  - rect.top  - size/2}px;
      position:absolute;border-radius:50%;
      background:rgba(255,255,255,0.15);
      transform:scale(0);animation:ripple .6s linear;
      pointer-events:none;z-index:999;
    `;
    if (getComputedStyle(target).position === 'static') target.style.position = 'relative';
    target.style.overflow = 'hidden';
    target.appendChild(circle);
    circle.addEventListener('animationend', () => circle.remove());
  });

  /* ── TOAST SYSTEM ── */
  window.vibeToast = (msg, type = 'info', duration = 3500) => {
    let container = document.querySelector('.toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'toast-container';
      document.body.appendChild(container);
    }
    const icons  = { info:'🎵', success:'✅', error:'❌', warning:'⚠️' };
    const colors = { info:'var(--cyan)', success:'var(--green)', error:'var(--rose)', warning:'var(--amber)' };
    const toast  = document.createElement('div');
    toast.className = 'toast-msg ' + type;
    toast.style.borderLeftColor = colors[type] || 'var(--cyan)';
    toast.innerHTML  = `
      <span style="font-size:1.1rem">${icons[type]||'🎵'}</span>
      <span style="flex:1">${msg}</span>
      <button onclick="this.parentElement.remove()" style="background:none;border:none;color:var(--txt-3);cursor:pointer;font-size:1.1rem;padding:0 0 0 8px;line-height:1">✕</button>
    `;
    container.appendChild(toast);
    // Progress bar inside toast
    const bar = document.createElement('div');
    bar.style.cssText = `position:absolute;bottom:0;left:0;height:2px;border-radius:2px;background:${colors[type]||'var(--cyan)'};width:100%;transform-origin:left;animation:none;transition:width ${duration}ms linear`;
    toast.style.position = 'relative';
    toast.appendChild(bar);
    setTimeout(() => { bar.style.width = '0'; }, 50);
    setTimeout(() => {
      toast.style.transition = 'opacity .35s, transform .35s';
      toast.style.opacity    = '0';
      toast.style.transform  = 'translateX(30px)';
      setTimeout(() => toast.remove(), 380);
    }, duration);
  };

  /* ── MINI PLAYER STATE ── */
  const playerState = {
    playing: false, progress: 32, volume: 75,
    liked: false, currentTrack: 0,
    tracks: [
      { name:'Pichincha Nightfall', artist:'MatS',           color:'f5a623', dur:'3:45' },
      { name:'Amanecer Neón',       artist:'DJ Santi',        color:'00e5ff', dur:'3:52' },
      { name:'Crimen Perfecto',     artist:'Guardarraya',     color:'8e44ad', dur:'3:15' },
      { name:'1537',                artist:'Guardarraya',     color:'22d3a5', dur:'4:05' },
      { name:'El Gran Retorno',     artist:'La Máq. Camaleón',color:'f59e0b', dur:'3:45' },
    ],
  };

  const player = document.querySelector('.mini-player');
  if (player) {
    const playBtn  = player.querySelector('.play-pause');
    const progFill = player.querySelector('.progress-fill');
    const progTrack= player.querySelector('.progress-track');
    const volFill  = player.querySelector('.vol-fill');
    const volTrack = player.querySelector('.vol-bar');
    const waveform = player.querySelector('.waveform');
    const likeBtn  = player.querySelector('.player-like-btn');
    const tName    = player.querySelector('.player-track-name');
    const tArtist  = player.querySelector('.player-track-artist');
    const thumb    = player.querySelector('.player-thumb');
    const tCurrent = player.querySelector('.time-current');

    const renderTrack = () => {
      const t = playerState.tracks[playerState.currentTrack];
      if (tName)   tName.textContent   = t.name;
      if (tArtist) tArtist.textContent = `${t.artist} • ${t.dur}`;
      if (thumb)   thumb.src = `https://placehold.co/52x52/${t.color}/0d1422?text=${encodeURIComponent(t.name[0])}`;
      // Sync sidebar
      const sbName  = document.getElementById('sidebar-np-name');
      const sbThumb = document.getElementById('sidebar-np-thumb');
      if (sbName)  sbName.textContent  = t.name;
      if (sbThumb) sbThumb.src = thumb?.src || '';
    };
    renderTrack();

    const togglePlay = () => {
      playerState.playing = !playerState.playing;
      const isPlaying = playerState.playing;
      if (playBtn) playBtn.innerHTML = isPlaying
        ? `<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M5.5 3.5A1.5 1.5 0 0 1 7 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5zm5 0A1.5 1.5 0 0 1 12 5v6a1.5 1.5 0 0 1-3 0V5a1.5 1.5 0 0 1 1.5-1.5z"/></svg>`
        : `<svg width="18" height="18" fill="currentColor" viewBox="0 0 16 16"><path d="M10.804 8 5 4.633v6.734L10.804 8zm.792-.696a.802.802 0 0 1 0 1.392l-6.363 3.692C4.713 12.69 4 12.345 4 11.692V4.308c0-.653.713-.998 1.233-.696l6.363 3.692z"/></svg>`;
      if (waveform) waveform.classList.toggle('playing', isPlaying);
      if (thumb)    thumb.classList.toggle('playing', isPlaying);
      document.querySelectorAll('#sidebar-waveform').forEach(w => w.classList.toggle('playing', isPlaying));
    };
    if (playBtn) playBtn.addEventListener('click', togglePlay);

    // Progress fill
    if (progFill) progFill.style.width = `${playerState.progress}%`;
    if (progTrack) {
      progTrack.addEventListener('click', e => {
        const rect = progTrack.getBoundingClientRect();
        playerState.progress = ((e.clientX - rect.left) / rect.width) * 100;
        if (progFill) progFill.style.width = `${playerState.progress}%`;
        const secs = Math.round(playerState.progress * 2.25);
        if (tCurrent) tCurrent.textContent = `${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;
      });
    }

    // Volume
    if (volFill)  volFill.style.width = `${playerState.volume}%`;
    if (volTrack) {
      volTrack.addEventListener('click', e => {
        const rect = volTrack.getBoundingClientRect();
        playerState.volume = ((e.clientX - rect.left) / rect.width) * 100;
        if (volFill) volFill.style.width = `${playerState.volume}%`;
      });
    }

    // Like
    if (likeBtn) {
      likeBtn.addEventListener('click', () => {
        playerState.liked = !playerState.liked;
        likeBtn.classList.toggle('liked', playerState.liked);
        likeBtn.innerHTML = playerState.liked
          ? `<svg width="16" height="16" fill="var(--rose)" viewBox="0 0 16 16"><path fill-rule="evenodd" d="M8 1.314C12.438-3.248 23.534 4.735 8 15-7.534 4.736 3.562-3.248 8 1.314z"/></svg>`
          : `<svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="m8 2.748-.717-.737C5.6.281 2.514.878 1.4 3.053c-.523 1.023-.641 2.5.314 4.385.92 1.815 2.834 3.989 6.286 6.357 3.452-2.368 5.365-4.542 6.286-6.357.955-1.886.838-3.362.314-4.385C13.486.878 10.4.28 8.717 2.01L8 2.748zM8 15C-7.333 4.868 3.279-3.04 8 2.066 12.72-3.04 23.333 4.868 8 15z"/></svg>`;
        vibeToast(playerState.liked ? 'Añadido a Me gusta ❤️' : 'Eliminado de Me gusta', playerState.liked ? 'success' : 'info');
      });
    }

    // Next / Prev
    player.querySelector('.btn-next')?.addEventListener('click', () => {
      playerState.currentTrack = (playerState.currentTrack + 1) % playerState.tracks.length;
      playerState.progress = 0;
      if (progFill) progFill.style.width = '0%';
      renderTrack();
      if (playerState.playing) {
        const t = playerState.tracks[playerState.currentTrack];
        vibeToast(`▶ ${t.name}`, 'info', 2000);
      }
    });
    player.querySelector('.btn-prev')?.addEventListener('click', () => {
      playerState.currentTrack = (playerState.currentTrack - 1 + playerState.tracks.length) % playerState.tracks.length;
      playerState.progress = 0;
      if (progFill) progFill.style.width = '0%';
      renderTrack();
    });

    // Auto-progress tick
    setInterval(() => {
      if (!playerState.playing) return;
      playerState.progress = Math.min(playerState.progress + 0.04, 100);
      if (progFill) progFill.style.width = `${playerState.progress}%`;
      const secs = Math.round(playerState.progress * 2.25);
      if (tCurrent) tCurrent.textContent = `${String(Math.floor(secs/60)).padStart(2,'0')}:${String(secs%60).padStart(2,'0')}`;
      if (playerState.progress >= 100) {
        playerState.currentTrack = (playerState.currentTrack + 1) % playerState.tracks.length;
        playerState.progress = 0;
        renderTrack();
      }
    }, 300);

    // Spacebar shortcut
    document.addEventListener('keydown', e => {
      if (e.code === 'Space' && !['INPUT','TEXTAREA','SELECT'].includes(e.target.tagName)) {
        e.preventDefault(); togglePlay();
      }
      if (e.code === 'ArrowRight' && e.altKey) player.querySelector('.btn-next')?.click();
      if (e.code === 'ArrowLeft'  && e.altKey) player.querySelector('.btn-prev')?.click();
    });
  }

  /* ── DRAG-TO-SCROLL on scroll rows ── */
  document.querySelectorAll('.scroll-row').forEach(row => {
    let isDown = false, startX, scrollLeft;
    row.addEventListener('mousedown',  e => { isDown = true; startX = e.pageX - row.offsetLeft; scrollLeft = row.scrollLeft; row.style.cursor = 'grabbing'; row.style.userSelect = 'none'; });
    row.addEventListener('mouseleave', () => { isDown = false; row.style.cursor = ''; });
    row.addEventListener('mouseup',    () => { isDown = false; row.style.cursor = ''; });
    row.addEventListener('mousemove',  e => {
      if (!isDown) return;
      e.preventDefault();
      row.scrollLeft = scrollLeft - (e.pageX - row.offsetLeft - startX) * 1.6;
    });
  });

  /* ── 3D TILT on music cards ── */
  document.querySelectorAll('.music-card .img-wrapper').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect = card.getBoundingClientRect();
      const x = (e.clientX - rect.left  - rect.width  / 2) / (rect.width  / 2);
      const y = (e.clientY - rect.top   - rect.height / 2) / (rect.height / 2);
      card.style.transform = `perspective(500px) rotateY(${x*9}deg) rotateX(${-y*9}deg) scale(1.05)`;
      card.style.transition = 'transform .05s';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform  = '';
      card.style.transition = 'transform .4s cubic-bezier(0.175,0.885,0.32,1.275)';
    });
  });

  /* ── PROGRESS BARS animate in ── */
  const barObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const bar = e.target;
      const w   = bar.dataset.width || bar.style.width;
      bar.style.width = '0';
      requestAnimationFrame(() => setTimeout(() => {
        bar.style.transition = 'width 1.3s cubic-bezier(0,0,0.2,1)';
        bar.style.width = w;
      }, 200));
      barObs.unobserve(bar);
    });
  }, { threshold: 0.3 });
  document.querySelectorAll('.progress-anim-bar, [data-progress]').forEach(b => barObs.observe(b));

  /* ── IMAGE UPLOAD PREVIEW ── */
  document.querySelectorAll('input[type="file"][accept*="image"]').forEach(input => {
    input.addEventListener('change', () => {
      const file = input.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = e => {
        const zone = input.closest('.upload-cover-zone');
        if (!zone) return;
        zone.style.backgroundImage    = `url(${e.target.result})`;
        zone.style.backgroundSize     = 'cover';
        zone.style.backgroundPosition = 'center';
        zone.querySelectorAll('svg, span:not(.music-note)').forEach(el => { el.style.opacity = '0'; el.style.transition = 'opacity .3s'; });
        vibeToast('Portada actualizada 🎨', 'success', 2000);
      };
      reader.readAsDataURL(file);
    });
  });

  /* ── PAGE-TRANSITION LINKS ── */
  document.querySelectorAll('a[href]:not([href^="#"]):not([href^="javascript"]):not([target])').forEach(link => {
    link.addEventListener('click', e => {
      const href = link.getAttribute('href');
      if (!href || href.startsWith('mailto') || href.startsWith('tel')) return;
      e.preventDefault();
      // Fade-out main content
      const main = document.querySelector('.main-content') || document.body;
      main.style.transition = 'opacity .28s ease, transform .28s ease';
      main.style.opacity    = '0';
      main.style.transform  = 'translateY(12px)';
      setTimeout(() => { window.location.href = href; }, 300);
    });
  });

  /* ── SKELETON SCREENS (auto replace empty cards) ── */
  function injectSkeleton(container, count = 4, type = 'music') {
    if (!container || container.children.length > 0) return;
    for (let i = 0; i < count; i++) {
      const sk = document.createElement('div');
      sk.className = 'music-card skeleton-card';
      sk.innerHTML = type === 'music'
        ? `<div class="skeleton" style="width:100%;aspect-ratio:1;border-radius:10px;margin-bottom:10px"></div>
           <div class="skeleton" style="height:13px;border-radius:4px;margin-bottom:6px"></div>
           <div class="skeleton" style="height:11px;border-radius:4px;width:65%"></div>`
        : `<div class="skeleton" style="width:100%;height:80px;border-radius:14px"></div>`;
      container.appendChild(sk);
    }
  }

  /* ── FORM VALIDATION GLOW ── */
  document.querySelectorAll('input[required], select[required], textarea[required]').forEach(el => {
    el.addEventListener('invalid', () => {
      el.style.borderColor = 'var(--rose)   !important';
      el.style.boxShadow   = '0 0 0 3px rgba(251,113,133,.2)';
    });
    el.addEventListener('input', () => { el.style.borderColor = ''; el.style.boxShadow = ''; });
  });

  /* ── MOBILE SIDEBAR CLOSE ── */
  document.addEventListener('click', e => {
    const sb = document.getElementById('sidebar');
    if (!sb) return;
    if (window.innerWidth <= 768 && sb.classList.contains('mobile-active')
        && !sb.contains(e.target) && !e.target.closest('#menuToggle')) {
      sb.classList.remove('mobile-active');
    }
  });

  /* ── FAQ TOGGLE (if present) ── */
  document.querySelectorAll('.faq-item').forEach(item => {
    item.addEventListener('click', () => {
      const answer = item.querySelector('.faq-answer');
      const arrow  = item.querySelector('.faq-arrow');
      if (!answer) return;
      const open = answer.style.display !== 'none';
      answer.style.display = open ? 'none' : 'block';
      if (arrow) arrow.style.transform = open ? '' : 'rotate(180deg)';
    });
  });

  /* ── AMBIENT PARTICLE EFFECT ── */
  function spawnParticle() {
    const p = document.createElement('div');
    const size = Math.random() * 3 + 1;
    const colors = ['#00e5ff','#a855f7','#22d3a5','#fbbf24','#fb7185'];
    p.style.cssText = `
      position:fixed;bottom:-10px;
      left:${Math.random()*100}%;
      width:${size}px;height:${size}px;
      border-radius:50%;
      background:${colors[Math.floor(Math.random()*colors.length)]};
      opacity:.5;pointer-events:none;z-index:0;
      animation:particle-float ${8+Math.random()*10}s ease-in-out forwards;
    `;
    document.body.appendChild(p);
    p.addEventListener('animationend', () => p.remove());
  }
  setInterval(spawnParticle, 2800);

  /* ── ACTIVE NAV LINK HIGHLIGHT ── */
  const currentPath = window.location.pathname;
  document.querySelectorAll('.nav-link-custom').forEach(link => {
    if (link.href && link.href.includes(currentPath) && currentPath !== '/') {
      link.classList.add('active');
    }
  });

  /* ── WELCOME TOAST ── */
  const pageTitle = document.title.replace('VibeSync — ', '').replace('VibeSync - ', '');
  const skipToast = ['Bienvenido','Login','Error'];
  if (pageTitle && !skipToast.some(s => pageTitle.includes(s))) {
    setTimeout(() => vibeToast(`Cargado: ${pageTitle} 🎵`, 'info', 2200), 900);
  }

});