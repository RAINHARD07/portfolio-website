const body = document.body;
const header = document.querySelector('.site-header');
const menuToggle = document.querySelector('.menu-toggle');
const navMenu = document.querySelector('.nav-menu');
const themeToggle = document.querySelector('.theme-toggle');
const themeIcon = document.querySelector('.theme-icon');
const backTopLinks = document.querySelectorAll('.back-top');
const apiBase = window.PORTFOLIO_API_BASE || '';

function csrfToken() {
  return document.cookie.split('; ').find((row) => row.startsWith('csrftoken='))?.split('=')[1] || '';
}

function escapeHtml(value) {
  return String(value ?? '').replace(/[&<>'"]/g, (character) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[character]));
}

async function getJson(path) {
  const response = await fetch(`${apiBase}${path}`, { headers: { Accept: 'application/json' }, credentials: 'same-origin' });
  if (!response.ok) throw new Error(`API request failed: ${response.status}`);
  return response.json();
}

if (themeToggle && themeIcon) {
  const savedTheme = localStorage.getItem('rainhard-theme');
  if (savedTheme === 'dark') body.dataset.theme = 'dark';
  updateThemeButton();
}

document.querySelectorAll('a[href*="instagram.com"]').forEach((link) => {
  const isFooterIcon = link.closest('.social-links');
  link.classList.add(isFooterIcon ? 'social-icon-image' : 'social-with-image');
  link.innerHTML = isFooterIcon
    ? '<img src="/static/site/Images/instagram.svg" alt="">'
    : '<img src="/static/site/Images/instagram.svg" alt=""> Instagram <span aria-hidden="true">&#8599;</span>';
});

const contactDetails = document.querySelector('.contact-details');
if (contactDetails && !contactDetails.querySelector('[href="tel:+233549924871"]')) {
  contactDetails.insertAdjacentHTML('beforeend', '<a href="tel:+233549924871"><span>PHONE 02</span>054 992 4871</a><a href="tel:+233503683840"><span>PHONE 03</span>050 368 3840</a>');
  contactDetails.querySelector('a[href^="mailto:"]')?.insertAdjacentHTML('afterbegin', '<span>EMAIL</span>');
  contactDetails.querySelector('a[href="tel:+233205378613"]')?.insertAdjacentHTML('afterbegin', '<span>PHONE 01</span>');
}

function updateThemeButton() {
  const isDark = body.dataset.theme === 'dark';
  if (themeIcon) themeIcon.textContent = isDark ? '\u2600' : '\u263d';
  if (themeToggle) themeToggle.setAttribute('aria-label', isDark ? 'Switch to light theme' : 'Switch to dark theme');
}

if (themeToggle) {
  themeToggle.addEventListener('click', () => {
    body.dataset.theme = body.dataset.theme === 'dark' ? 'light' : 'dark';
    localStorage.setItem('rainhard-theme', body.dataset.theme);
    updateThemeButton();
  });
}

if (menuToggle && navMenu) {
  menuToggle.addEventListener('click', () => {
    const isOpen = navMenu.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(isOpen));
  });

  document.querySelectorAll('.nav-menu a').forEach((link) => {
    link.addEventListener('click', () => {
      navMenu.classList.remove('open');
      menuToggle.setAttribute('aria-expanded', 'false');
    });
  });
}

const revealObserver = new IntersectionObserver((entries, observer) => {
  entries.forEach((entry) => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

const sections = [...document.querySelectorAll('main section[id]')];
const navLinks = [...document.querySelectorAll('.nav-menu a[href^="#"]')];
const sectionObserver = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`));
  });
}, { rootMargin: '-30% 0px -62% 0px' });
sections.forEach((section) => sectionObserver.observe(section));

window.addEventListener('scroll', () => header.classList.toggle('scrolled', window.scrollY > 18), { passive: true });

backTopLinks.forEach((link) => {
  link.addEventListener('click', (event) => {
    event.preventDefault();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    header.focus({ preventScroll: true });
  });
});

const filters = document.querySelectorAll('.filter');
let projects = document.querySelectorAll('.project-card');
filters.forEach((filter) => {
  filter.addEventListener('click', () => {
    filters.forEach((button) => button.classList.remove('active'));
    filter.classList.add('active');
    const selected = filter.dataset.filter;
    projects.forEach((project) => project.classList.toggle('is-hidden', selected !== 'all' && project.dataset.category !== selected));
  });
});

async function loadPortfolioData() {
  try {
    const [projectResponse, skillResponse] = await Promise.all([getJson('/api/projects?limit=20'), getJson('/api/skills')]);
    if (projectResponse.data?.length) {
      const projectGrid = document.querySelector('.project-grid');
      projectGrid.innerHTML = projectResponse.data.map((project, index) => `
        <article class="project-card ${project.featured ? 'project-featured' : ''} reveal ${index % 2 ? 'reveal-delay' : ''}" data-category="${escapeHtml(project.category.toLowerCase().replaceAll(' ', '-'))}">
          <div class="project-meta"><span>${String(index + 1).padStart(2, '0')} / Project</span><span>${escapeHtml(project.category)}</span></div>
          <h3>${escapeHtml(project.title)}</h3>
          <div class="case-study"><p><b>Summary</b> ${escapeHtml(project.description)}</p><p><b>Stack</b> ${escapeHtml((project.techStack || []).join(', '))}</p></div>
          <a href="#contact" class="project-link" data-project="${escapeHtml(project.title)}" aria-label="Discuss ${escapeHtml(project.title)}">Discuss this project <span aria-hidden="true">&#8599;</span></a>
        </article>`).join('');
      projects = document.querySelectorAll('.project-card');
      projects.forEach((project) => project.classList.add('visible'));
      document.querySelectorAll('.project-link[data-project]').forEach((link) => link.addEventListener('click', () => {
        const message = document.querySelector('#message');
        if (message) message.value = `I'd like to discuss the ${link.dataset.project} project.`;
      }));
    }
    if (skillResponse.data?.length) {
      const skillGrid = document.querySelector('.skills-grid');
      skillGrid.innerHTML = skillResponse.data.map((skill, index) => `
        <article class="skill-item visible"><div class="skill-head"><span>${String(index + 1).padStart(2, '0')}</span><h3>${escapeHtml(skill.name)}</h3><b>${escapeHtml(skill.proficiencyLevel)}%</b></div><p>${escapeHtml(skill.category)}</p><div class="meter"><span style="--level:${Math.min(Number(skill.proficiencyLevel) || 0, 100)}%"></span></div></article>`).join('');
    }
  } catch (error) {
    console.warn('Portfolio API unavailable; using the embedded portfolio content.', error);
  }
}
loadPortfolioData();

document.querySelectorAll('.project-link[data-project]').forEach((link) => {
  link.addEventListener('click', () => {
    const message = document.querySelector('#message');
    if (!message) return;
    message.value = `I'd like to discuss the ${link.dataset.project} project.`;
  });
});

const statsBand = document.querySelector('.stats-band');
const counters = [...document.querySelectorAll('[data-count]')];
let countersStarted = false;
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const setCounterValues = () => counters.forEach((counter) => {
  counter.textContent = counter.dataset.count || '0';
});
const animateCounters = () => {
  if (countersStarted) return;
  countersStarted = true;
  if (prefersReducedMotion) {
    setCounterValues();
    return;
  }
  const duration = 1000;
  const start = performance.now();
  const tick = (now) => {
    const progress = Math.min((now - start) / duration, 1);
    counters.forEach((counter) => {
      counter.textContent = String(Math.floor(progress * Number(counter.dataset.count)));
    });
    if (progress < 1) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
};
setCounterValues();
if (statsBand) {
  const counterObserver = new IntersectionObserver((entries, observer) => {
    if (entries.some((entry) => entry.isIntersecting)) {
      animateCounters();
      observer.disconnect();
    }
  }, { threshold: 0.15 });
  counterObserver.observe(statsBand);
}

const form = document.querySelector('#contact-form');
if (form) {
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const status = form.querySelector('.form-status');
    if (!form.checkValidity()) {
      if (status) status.textContent = 'Please complete your name, email and message.';
      form.reportValidity();
      return;
    }
    const data = new FormData(form);
    if (status) status.textContent = 'Sending your message...';
    try {
      const response = await fetch(`${apiBase}/api/messages`, {
        method: 'POST',
        credentials: 'same-origin',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken(), Accept: 'application/json' },
        body: JSON.stringify({ name: data.get('name'), email: data.get('email'), subject: 'Portfolio enquiry', message: data.get('message') }),
      });
      if (!response.ok) throw new Error('Message request failed');
      form.reset();
      if (status) status.textContent = 'Message sent. Thank you for reaching out.';
    } catch (error) {
      if (status) status.textContent = 'The message could not be sent. Please email me directly.';
      console.error(error);
    }
  });
}

fetch(`${apiBase}/api/analytics/visit`, {
  method: 'POST',
  keepalive: true,
  credentials: 'same-origin',
  headers: { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken(), Accept: 'application/json' },
  body: JSON.stringify({ pageVisited: window.location.pathname, referrer: document.referrer }),
}).catch(() => {});
