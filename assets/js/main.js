(() => {
  const menuButton = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.site-nav');
  menuButton?.addEventListener('click', () => {
    const expanded = menuButton.getAttribute('aria-expanded') === 'true';
    menuButton.setAttribute('aria-expanded', String(!expanded));
    nav?.classList.toggle('open', !expanded);
  });

  const filters = document.querySelectorAll('[data-filter]');
  const publications = document.querySelectorAll('.pub-item');
  filters.forEach((button) => button.addEventListener('click', () => {
    filters.forEach((b) => b.classList.remove('active'));
    button.classList.add('active');
    const filter = button.dataset.filter;
    publications.forEach((item) => {
      item.hidden = !(filter === 'all' || item.dataset.type === filter);
    });
    document.querySelectorAll('.year-group').forEach((year) => {
      year.hidden = !Array.from(year.querySelectorAll('.pub-item')).some((item) => !item.hidden);
    });
  }));
})();
