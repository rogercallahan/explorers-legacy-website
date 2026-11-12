/* Progressive enhancement only: no network, accounts, cookies or journal storage. */
(() => {
  'use strict';
  const expeditions = Array.from(document.querySelectorAll('.expedition'));
  const search = document.getElementById('expedition-search');
  const index = Array.from(document.querySelectorAll('.expedition-index li'));
  const count = document.getElementById('expedition-count');
  function filter() {
    const query = search.value.trim().toLocaleLowerCase();
    let visible = 0;
    expeditions.forEach((entry, i) => {
      const match = (entry.id + ' ' + entry.dataset.title).toLocaleLowerCase().includes(query);
      entry.hidden = !match;
      if (index[i]) index[i].hidden = !match;
      if (match) visible += 1;
    });
    count.textContent = visible ? visible + ' of 25 expeditions' : 'No matches. Clear the search to see all 25.';
  }
  if (search) {
    document.querySelector('.expedition-search').hidden = false;
    search.addEventListener('input', filter);
    document.getElementById('clear-search').addEventListener('click', () => {
      search.value = ''; filter(); search.focus();
    });
  }
  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch (_) { return; }
    const entry = document.getElementById(id);
    if (!entry || !entry.classList.contains('expedition')) return;
    if (search) { search.value = ''; filter(); }
    entry.open = true;
    entry.scrollIntoView({block:'start', behavior:'instant'});
  }
  addEventListener('hashchange', revealHash);
  document.querySelectorAll('a[href^="#"]').forEach(link => link.addEventListener('click', () => {
    if (link.hash === location.hash) revealHash();
  }));
  revealHash();
  let printState = null;
  addEventListener('beforeprint', () => {
    if (printState) return;
    printState = expeditions.map(entry => ({entry, open:entry.open, hidden:entry.hidden}));
    expeditions.forEach(entry => {entry.open = true; entry.hidden = false;});
  });
  addEventListener('afterprint', () => {
    if (printState) printState.forEach(({entry,open,hidden}) => {entry.open=open;entry.hidden=hidden;});
    printState = null;
    document.body.classList.remove('print-one');
    expeditions.forEach(entry => entry.classList.remove('print-selected'));
  });
  document.querySelectorAll('.print-expedition').forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      const entry = document.getElementById(button.dataset.expedition);
      if (!entry) return;
      entry.classList.add('print-selected');
      document.body.classList.add('print-one');
      window.print();
    });
  });
})();
