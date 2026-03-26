document.addEventListener('DOMContentLoaded', () => {

    const reveals = document.querySelectorAll('.reveal');
    const revealOptions = { threshold: 0.1, rootMargin: "0px 0px -50px 0px" };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        });
    }, revealOptions);

    reveals.forEach(reveal => { revealOnScroll.observe(reveal); });

    const accordionHeaders = document.querySelectorAll('.accordion-header');
    accordionHeaders.forEach(header => {
        header.addEventListener('click', () => {
            const content = header.nextElementSibling;
            const icon = header.querySelector('.icon');
            const isActive = content.style.maxHeight;

            document.querySelectorAll('.accordion-content').forEach(item => { item.style.maxHeight = null; });
            document.querySelectorAll('.accordion-header .icon').forEach(i => { i.textContent = '+'; });

            if (!isActive) {
                content.style.maxHeight = content.scrollHeight + "px";
                icon.textContent = '−';
            }
        });
    });

    const modal = document.getElementById('caseModal');
    const closeBtn = document.querySelector('.close-modal');
    const cards = document.querySelectorAll('.portfolio-card');

    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDesc');
    const modalStack = document.getElementById('modalStack');
    const modalImage = document.getElementById('modalImage');
    
    // Элементы для ссылок
    const resourcesBlock = document.getElementById('modalResourcesBlock');
    const linksContainer = document.getElementById('modalLinks');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            modalTitle.innerText = card.dataset.title || 'Название кейса';
            modalDesc.innerText = card.dataset.desc || 'Описание отсутствует.';
            modalStack.innerText = card.dataset.stack || 'Стек не указан.';

            // Обработка ссылок
            const githubLink = card.dataset.github;
            const liveLink = card.dataset.live;
            
            linksContainer.innerHTML = '';
            
            if (githubLink || liveLink) {
                resourcesBlock.style.display = 'block';
                if (githubLink) linksContainer.innerHTML += `<a href="${githubLink}" target="_blank" style="text-decoration: underline; font-weight: 500;">GitHub</a>`;
                if (liveLink) linksContainer.innerHTML += `<a href="${liveLink}" target="_blank" style="text-decoration: underline; font-weight: 500;">Live</a>`;
            } else {
                resourcesBlock.style.display = 'none';
            }

            if (card.dataset.img && card.dataset.img.trim() !== '') {
                modalImage.innerHTML = `<img src="${card.dataset.img}" style="width: 100%; height: 100%; object-fit: cover; border-radius: 4px; border: 1px solid var(--border-color);">`;
                modalImage.style.backgroundColor = 'transparent';
            } else {
                modalImage.innerHTML = 'Превью кейса';
                modalImage.style.backgroundColor = 'var(--surface-color)';
            }

            modal.style.display = 'block';
            setTimeout(() => modal.classList.add('show'), 10);
            document.body.style.overflow = 'hidden'; 
        });
    });

    const closeModal = () => {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
        }, 300);
    };

    closeBtn.addEventListener('click', closeModal);
    window.addEventListener('click', (e) => { if (e.target === modal) closeModal(); });

    const form = document.getElementById('contactForm');
    const statusText = document.getElementById('form-status');

    if(form) {
        form.addEventListener('submit', (e) => {
            e.preventDefault();

            const name = sanitizeInput(document.getElementById('name').value);
            const email = sanitizeInput(document.getElementById('email').value);
            const message = sanitizeInput(document.getElementById('message').value);

            if (!name || !email || !message) {
                statusText.style.color = '#ff4444';
                statusText.innerText = 'Пожалуйста, заполните все поля.';
                return;
            }

            statusText.style.color = '#44ff44';
            statusText.style.marginTop = '15px';
            statusText.innerText = 'Сообщение успешно отправлено!';
            form.reset();

            setTimeout(() => { statusText.innerText = ''; }, 5000);
        });
    }

    function sanitizeInput(input) {
        const div = document.createElement('div');
        div.textContent = input;
        return div.innerHTML.trim();
    }
});