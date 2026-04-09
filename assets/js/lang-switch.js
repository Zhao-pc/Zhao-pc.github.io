(function () {
  const STORAGE_KEY = 'preferred-lang';

  function applyLang(lang) {
    const enEls = document.querySelectorAll('.lang-en');
    const zhEls = document.querySelectorAll('.lang-zh');
    const btn = document.getElementById('lang-toggle');

    enEls.forEach(el => el.style.display = lang === 'en' ? '' : 'none');
    zhEls.forEach(el => el.style.display = lang === 'zh' ? '' : 'none');

    if (btn) {
      btn.textContent = lang === 'en' ? '中文' : 'English';
    }

    localStorage.setItem(STORAGE_KEY, lang);
  }

  window.toggleLang = function () {
    const current = localStorage.getItem(STORAGE_KEY) || 'en';
    applyLang(current === 'en' ? 'zh' : 'en');
  };

  // 页面加载时读取用户偏好
  document.addEventListener('DOMContentLoaded', function () {
    const saved = localStorage.getItem(STORAGE_KEY) || 'en';
    applyLang(saved);
  });
})();
