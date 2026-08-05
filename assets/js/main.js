(() => {
  const root = document.documentElement;
  const themeButton = document.querySelector('.theme-toggle');
  const updateThemeLabel = () => {
    if (themeButton) themeButton.setAttribute('aria-label', root.dataset.theme === 'dark' ? 'Use light mode' : 'Use dark mode');
  };
  themeButton?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('theme', root.dataset.theme);
    updateThemeLabel();
  });
  updateThemeLabel();

  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    nav?.classList.toggle('open', !expanded);
  });

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));

  const filters = document.querySelectorAll('[data-filter]');
  const publications = document.querySelectorAll('.pub-item');
  filters.forEach((button) => button.addEventListener('click', () => {
    filters.forEach((b) => b.classList.remove('active'));
    button.classList.add('active');
    const filter = button.dataset.filter;
    publications.forEach((item) => {
      const visible = filter === 'all' || item.dataset.type === filter;
      item.hidden = !visible;
    });
    document.querySelectorAll('.pub-year').forEach((year) => {
      year.hidden = !Array.from(year.querySelectorAll('.pub-item')).some((item) => !item.hidden);
    });
  }));
})();
