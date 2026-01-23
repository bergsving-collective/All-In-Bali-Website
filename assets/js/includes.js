const includeTargets = [
    { id: 'site-nav', path: 'nav.html' },
    { id: 'site-footer', path: 'footer.html' },
    { id: 'site-whatsapp', path: 'whatsapp.html' }
];

const loadInclude = async ({ id, path }) => {
    const target = document.getElementById(id);
    if (!target) return;

    try {
        const response = await fetch(path, { cache: 'no-cache' });
        if (!response.ok) throw new Error(`Failed to load ${path}`);
        target.innerHTML = await response.text();
    } catch (error) {
        console.error(error);
    }
};

const initMobileMenu = () => {
    const mobileBtn = document.getElementById('mobileMenuButton');
    const mobileMenu = document.getElementById('mobileMenu');
    if (!mobileBtn || !mobileMenu) return;

    mobileBtn.addEventListener('click', function () {
        mobileMenu.classList.toggle('hidden');
        const expanded = this.getAttribute('aria-expanded') === 'true';
        this.setAttribute('aria-expanded', (!expanded).toString());
    });
};

window.addEventListener('DOMContentLoaded', async () => {
    await Promise.all(includeTargets.map(loadInclude));
    initMobileMenu();
});
