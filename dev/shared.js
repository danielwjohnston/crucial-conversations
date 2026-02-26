/* ============================================================
   shared.js — Single source of truth for all slidedeck behavior
   Leadership Bookclub — Crucial Conversations

   USAGE: Each chapter HTML must define two globals BEFORE loading this script:
     const CURRENT_CHAPTER_INDEX = 11;          // 0-based index
     const DURATIONS_SECONDS = [30, 90, ...];   // per-slide durations
   ============================================================ */

// ============================================================
// CHAPTERS DATA
// ============================================================
const CHAPTERS = [
    { num: 1,  file: "chapter_01_crucial_conversation.html",  title: "What\u2019s a Crucial Conversation", subtitle: "And who cares?", part: 1 },
    { num: 2,  file: "chapter_02_mastering_conversations.html", title: "Mastering Crucial Conversations", subtitle: "The power of dialogue", part: 1 },
    { num: 3,  file: "chapter_03_choose_topic.html",          title: "Choose Your Topic", subtitle: "How to be sure you hold the right conversation", part: 1 },
    { num: 4,  file: "chapter_04_start_heart.html",           title: "Start with Heart", subtitle: "How to stay focused on what you really want", part: 1 },
    { num: 5,  file: "chapter_05_master_stories.html",        title: "Master My Stories", subtitle: "How to stay in dialogue when you\u2019re angry, scared, or hurt", part: 2 },
    { num: 6,  file: "chapter_06_learn_to_look.html",         title: "Learn to Look", subtitle: "How to notice when safety is at risk", part: 2 },
    { num: 7,  file: "chapter_07_make_safe.html",             title: "Make It Safe", subtitle: "How to make it safe to talk about almost anything", part: 2 },
    { num: 8,  file: "chapter_08_state_path.html",            title: "STATE My Path", subtitle: "How to speak persuasively, not abrasively", part: 2 },
    { num: 9,  file: "chapter_09_explore_paths.html",         title: "Explore Others\u2019 Paths", subtitle: "How to listen when others blow up or clam up", part: 2 },
    { num: 10, file: "chapter_10_retake_pen.html",            title: "Retake Your Pen", subtitle: "How to be resilient and hear almost anything", part: 2 },
    { num: 11, file: "chapter_11_move_action.html",           title: "Move to Action", subtitle: "How to turn crucial conversations into action and results", part: 3 },
    { num: 12, file: "chapter_12_yeah_but.html",              title: "Yeah, But", subtitle: "Advice for tough cases", part: 3 },
    { num: 13, file: "chapter_13_putting_together.html",      title: "Putting It All Together", subtitle: "Tools for preparing and learning", part: 3 },
];

const PART_LABELS = {
    1: "Part I \u2014 Before You Open Your Mouth",
    2: "Part II \u2014 How to Open Your Mouth",
    3: "Part III \u2014 How to Finish"
};

// ============================================================
// CHAPTER DROPDOWN
// ============================================================
function buildDropdown() {
    const menu = document.getElementById('dropdownMenu');
    menu.innerHTML = '';
    let currentPart = 0;
    CHAPTERS.forEach((ch, idx) => {
        if (ch.part !== currentPart) {
            currentPart = ch.part;
            if (idx > 0) {
                const divider = document.createElement('div');
                divider.className = 'dropdown-divider';
                menu.appendChild(divider);
            }
            const label = document.createElement('div');
            label.className = 'dropdown-section-label';
            label.textContent = PART_LABELS[currentPart];
            menu.appendChild(label);
        }
        const item = document.createElement('div');
        item.className = 'chapter-dropdown-item' + (idx === CURRENT_CHAPTER_INDEX ? ' active' : '');
        item.setAttribute('role', 'menuitem');
        item.setAttribute('tabindex', '0');
        item.innerHTML = '<span class="ch-num">' + ch.num + '</span><span class="ch-info"><span class="ch-title">' + ch.title + '</span><span class="ch-subtitle">' + ch.subtitle + '</span></span>';
        item.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); closeDropdown(); if (idx !== CURRENT_CHAPTER_INDEX) window.location.href = ch.file; });
        item.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); closeDropdown(); if (idx !== CURRENT_CHAPTER_INDEX) window.location.href = ch.file; } });
        menu.appendChild(item);
    });
    const divider = document.createElement('div');
    divider.className = 'dropdown-divider';
    menu.appendChild(divider);
    const backItem = document.createElement('div');
    backItem.className = 'chapter-dropdown-item';
    backItem.setAttribute('role', 'menuitem');
    backItem.setAttribute('tabindex', '0');
    backItem.innerHTML = '<span class="ch-num" style="background:#333;color:white;border-color:#333;">\u2630</span><span class="ch-info"><span class="ch-title">Back to Chapter Select</span></span>';
    backItem.addEventListener('click', (e) => { e.preventDefault(); e.stopPropagation(); window.location.href = '../index.html'; });
    backItem.addEventListener('keydown', (e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); window.location.href = '../index.html'; } });
    menu.appendChild(backItem);
}

const dropdownBtn = document.getElementById('dropdownBtn');
const dropdownMenu = document.getElementById('dropdownMenu');

function toggleDropdown() { const isOpen = dropdownMenu.classList.contains('open'); if (isOpen) closeDropdown(); else openDropdown(); }
function openDropdown() { dropdownMenu.classList.add('open'); dropdownBtn.classList.add('open'); dropdownBtn.setAttribute('aria-expanded', 'true'); }
function closeDropdown() { dropdownMenu.classList.remove('open'); dropdownBtn.classList.remove('open'); dropdownBtn.setAttribute('aria-expanded', 'false'); }
dropdownBtn.addEventListener('click', toggleDropdown);
document.addEventListener('click', (e) => { if (!e.target.closest('.chapter-dropdown-wrapper')) closeDropdown(); });

// ============================================================
// SLIDE ENGINE
// ============================================================
let currentSlide = 0;
const slides = document.querySelectorAll('.slide');
const totalSlides = slides.length;
const chapterHeader = document.getElementById('chapterHeader');
const timerContainer = document.getElementById('timerContainer');
const timerText = document.getElementById('timerText');
const timerCircle = document.getElementById('timerCircle');
const autoAdvanceToggle = document.querySelector('.auto-advance-toggle');
const timerAria = document.getElementById('timerAria');

let autoAdvanceEnabled = false;
let countdownInterval = null;
let remainingTime = 0;
let totalDuration = 0;
let lastAnnouncement = -1;

document.getElementById('totalSlides').textContent = totalSlides;

// ============================================================
// DIGEST MODALS
// ============================================================
function openDigest(n) {
    const modal = document.getElementById('digestModal' + n);
    if (!modal) return;
    modal.classList.add('active');
    const closeBtn = modal.querySelector('.digest-close');
    if (closeBtn) closeBtn.focus();
}

function closeDigest(n) {
    const modal = document.getElementById('digestModal' + n);
    if (!modal) return;
    modal.classList.remove('active');
}

function closeAllDigests() {
    document.querySelectorAll('.digest-modal.active').forEach((modal) => modal.classList.remove('active'));
}

document.querySelectorAll('.digest-modal').forEach((modal) => {
    modal.addEventListener('click', (e) => { if (e.target === modal) modal.classList.remove('active'); });
});

// ============================================================
// AUTO-ADVANCE TIMER
// ============================================================
function getSlideDuration() { return DURATIONS_SECONDS[currentSlide] ?? 60; }

function formatTime(seconds) {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return mins + ':' + secs.toString().padStart(2, '0');
}

function updateTimerCircle() {
    const circumference = 163.36;
    const progress = remainingTime / totalDuration;
    const offset = circumference * (1 - progress);
    timerCircle.style.strokeDashoffset = offset;
}

function announceTimer(msg) { if (timerAria) timerAria.textContent = msg; }

function startTimer() {
    if (!autoAdvanceEnabled) return;
    stopTimer();
    totalDuration = getSlideDuration();
    remainingTime = totalDuration;
    lastAnnouncement = -1;
    timerText.textContent = formatTime(remainingTime);
    updateTimerCircle();
    countdownInterval = setInterval(() => {
        remainingTime--;
        timerText.textContent = formatTime(remainingTime);
        updateTimerCircle();
        if (remainingTime % 60 === 0 || (remainingTime < 60 && remainingTime % 10 === 0)) {
            if (remainingTime !== lastAnnouncement) { announceTimer(formatTime(remainingTime) + ' remaining'); lastAnnouncement = remainingTime; }
        }
        if (remainingTime <= 0) { stopTimer(); nextSlide(); }
    }, 1000);
}

function stopTimer() { if (countdownInterval) { clearInterval(countdownInterval); countdownInterval = null; } }

function toggleAutoAdvance() {
    autoAdvanceEnabled = !autoAdvanceEnabled;
    if (autoAdvanceEnabled) {
        autoAdvanceToggle.innerHTML = '<span aria-hidden="true">\u23F8</span> Auto-Advance: ON';
        autoAdvanceToggle.setAttribute('aria-pressed', 'true');
        autoAdvanceToggle.classList.add('active');
        timerContainer.classList.add('active');
        startTimer();
    } else {
        autoAdvanceToggle.innerHTML = '<span aria-hidden="true">\u25B6</span> Auto-Advance: OFF';
        autoAdvanceToggle.setAttribute('aria-pressed', 'false');
        autoAdvanceToggle.classList.remove('active');
        timerContainer.classList.remove('active');
        stopTimer();
    }
}

// ============================================================
// SLIDE NAVIGATION
// ============================================================
function showSlide(n) {
    slides[currentSlide].classList.remove('active');
    slides[currentSlide].classList.remove('with-header');
    slides[currentSlide].removeAttribute('tabindex');
    currentSlide = Math.max(0, Math.min(n, totalSlides - 1));
    slides[currentSlide].classList.add('active');
    if (currentSlide === 0) { chapterHeader.classList.remove('show'); }
    else { chapterHeader.classList.add('show'); slides[currentSlide].classList.add('with-header'); }
    document.getElementById('slideNumber').textContent = currentSlide + 1;
    slides[currentSlide].setAttribute('tabindex', '-1');
    slides[currentSlide].focus();
    if (autoAdvanceEnabled) startTimer();
}

function nextSlide() {
    closeAllDigests();
    if (currentSlide < totalSlides - 1) { showSlide(currentSlide + 1); }
    else if (CURRENT_CHAPTER_INDEX < CHAPTERS.length - 1) { window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX + 1].file; }
}

function previousSlide() {
    closeAllDigests();
    if (currentSlide > 0) { showSlide(currentSlide - 1); }
    else if (CURRENT_CHAPTER_INDEX > 0) { window.location.href = CHAPTERS[CURRENT_CHAPTER_INDEX - 1].file + '?slide=last'; }
}

// ============================================================
// KEYBOARD NAVIGATION
// ============================================================
document.addEventListener('keydown', function(event) {
    if (event.target.closest('.chapter-dropdown-menu')) return;
    const anyDigestOpen = !!document.querySelector('.digest-modal.active');
    if (event.key === 'Escape') { if (anyDigestOpen) closeAllDigests(); else closeDropdown(); return; }
    if (event.key === 'ArrowLeft') { previousSlide(); }
    else if (event.key === 'ArrowRight') { nextSlide(); }
    else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        if (anyDigestOpen) { closeAllDigests(); return; }
        const activeSlide = document.querySelector('.slide.active');
        const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest]');
        if (digestBtn) { const id = digestBtn.getAttribute('data-digest'); if (id) openDigest(Number(id)); }
    }
    else if (event.key === 'a' || event.key === 'A') { toggleAutoAdvance(); }
    else if (event.key === 'd' || event.key === 'D') {
        if (anyDigestOpen) { closeAllDigests(); return; }
        const activeSlide = document.querySelector('.slide.active');
        const digestBtn = activeSlide?.querySelector('.digest-pill[data-digest]');
        if (digestBtn) { const id = digestBtn.getAttribute('data-digest'); if (id) openDigest(Number(id)); }
    }
});

// ============================================================
// DEEP LINKING — ?slide=X or ?slide=last
// ============================================================
function handleURLParams() {
    const params = new URLSearchParams(window.location.search);
    const sl = params.get('slide');
    if (sl === 'last') { showSlide(totalSlides - 1); return true; }
    else if (sl) { const idx = parseInt(sl) - 1; if (idx >= 0 && idx < totalSlides) { showSlide(idx); return true; } }
    return false;
}

// ============================================================
// TERM TOOLTIP (fixed-position, escapes overflow)
// ============================================================
(function() {
    let tip = null;
    function show(e) {
        const def = e.target.dataset.def;
        if (!def) return;
        if (!tip) {
            tip = document.createElement('div');
            tip.className = 'term-tip';
            tip.innerHTML = '<span class="term-tip-arrow"></span><span class="term-tip-text"></span>';
            document.body.appendChild(tip);
        }
        const arrow = tip.querySelector('.term-tip-arrow');
        tip.querySelector('.term-tip-text').textContent = def;
        tip.classList.remove('visible');
        tip.style.left = '0'; tip.style.top = '0';
        tip.style.display = 'block';
        const r = e.target.getBoundingClientRect();
        const tw = tip.offsetWidth, th = tip.offsetHeight;
        let left = r.left + r.width / 2 - tw / 2;
        left = Math.max(8, Math.min(left, window.innerWidth - tw - 8));
        const above = r.top - th - 10;
        if (above > 4) {
            tip.style.top = above + 'px';
            arrow.className = 'term-tip-arrow above';
        } else {
            tip.style.top = (r.bottom + 10) + 'px';
            arrow.className = 'term-tip-arrow below';
        }
        tip.style.left = left + 'px';
        arrow.style.left = (r.left + r.width / 2 - left) + 'px';
        arrow.style.transform = 'translateX(-50%)';
        requestAnimationFrame(function(){ tip.classList.add('visible'); });
    }
    function hide() { if (tip) { tip.classList.remove('visible'); tip.style.display = 'none'; } }
    document.addEventListener('mouseover', function(e){ if (e.target.classList.contains('term')) show(e); });
    document.addEventListener('mouseout',  function(e){ if (e.target.classList.contains('term')) hide(); });
    document.addEventListener('focusin',   function(e){ if (e.target.classList.contains('term')) show(e); });
    document.addEventListener('focusout',  function(e){ if (e.target.classList.contains('term')) hide(); });
})();

// ============================================================
// INIT
// ============================================================
buildDropdown();
if (!handleURLParams()) showSlide(0);
