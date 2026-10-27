(() => {
    'use strict';
    const products = window.PRODUTOS || [];
    const byId = new Map(products.map(p => [p.id, p]));
    const money = cents => (cents / 100).toLocaleString('pt-BR', { style: 'currency', currency: 'BRL' });
    const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
    const root = new URL('../../', document.currentScript.src);
    const key = 'paradox-carrinho-v1';
    const notice = document.querySelector('#aviso-global');
    let timer;
    function announce(message) {
        if (!notice) return;
        notice.textContent = message;
        notice.classList.add('visivel');
        clearTimeout(timer);
        timer = setTimeout(() => notice.classList.remove('visivel'), 4500);
    }
    let cart = [];
    function cleanCart(value) {
        if (!Array.isArray(value)) return [];
        const unique = new Map();
        value.forEach(item => {
            if (item && byId.has(item.id) && Number.isInteger(item.quantity) && item.quantity > 0)
                unique.set(item.id, { id: item.id, quantity: Math.min(99, item.quantity) });
        });
        return [...unique.values()];
    }
    try { cart = cleanCart(JSON.parse(localStorage.getItem(key) || '[]')); } catch { /* Começa vazio se os dados estiverem indisponíveis. */ }
    function save() {
        try { localStorage.setItem(key, JSON.stringify(cart)); }
        catch { announce('O navegador não permite salvar o carrinho entre páginas. Habilite o armazenamento local.'); return false; }
        updateCount(); return true;
    }
    function updateCount() {
        const total = cart.reduce((sum, item) => sum + item.quantity, 0);
        document.querySelectorAll('.quantidade-carrinho').forEach(el => el.textContent = total);
        document.querySelectorAll('.link-carrinho').forEach(el => el.setAttribute('aria-label', `Abrir carrinho de compras: ${total} itens`));
    }
    document.addEventListener('click', event => {
        const button = event.target.closest('[data-adicionar]');
        if (!button) return;
        const product = byId.get(button.dataset.adicionar);
        if (!product) return;
        const item = cart.find(entry => entry.id === product.id);
        if (item && item.quantity >= 99) return announce('Limite de 99 unidades por produto.');
        if (item) item.quantity++; else cart.push({ id: product.id, quantity: 1 });
        if (save()) announce(`${product.name} adicionado ao carrinho.`);
    });
    window.addEventListener('storage', event => {
        if (event.key !== key) return;
        try { cart = cleanCart(JSON.parse(event.newValue || '[]')); } catch { cart = []; }
        updateCount(); renderCart();
    });
    updateCount();

    // Carrossel manual para não interromper a leitura dos destaques.
    const carousel = document.querySelector('.carrossel');
    if (carousel) {
        const slides = [...carousel.querySelectorAll('.slide')];
        const indicators = [...carousel.querySelectorAll('.indicador-slide')];
        let active = 0;
        carousel.setAttribute('aria-roledescription', 'carrossel');
        const status = document.createElement('p');
        status.className = 'sr-only'; status.setAttribute('aria-live', 'polite'); carousel.append(status);
        function show(index, speak = true) {
            active = (index + slides.length) % slides.length;
            slides.forEach((slide, i) => {
                slide.classList.toggle('ativo', i === active); slide.hidden = i !== active;
                slide.setAttribute('aria-label', `Destaque ${i + 1} de ${slides.length}`);
            });
            indicators.forEach((button, i) => {
                button.classList.toggle('ativo', i === active);
                if (i === active) button.setAttribute('aria-current', 'true'); else button.removeAttribute('aria-current');
            });
            if (speak) status.textContent = `Destaque ${active + 1} de ${slides.length}`;
        }
        carousel.querySelector('.seta-anterior').addEventListener('click', () => show(active - 1));
        carousel.querySelector('.seta-proxima').addEventListener('click', () => show(active + 1));
        indicators.forEach((button, i) => button.addEventListener('click', () => show(i)));
        carousel.addEventListener('keydown', event => {
            if (event.target.closest('a,input')) return;
            if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') { event.preventDefault(); show(active + (event.key === 'ArrowRight' ? 1 : -1)); }
        });
        show(0, false);
    }

    const filters = document.querySelector('#filtros');
    if (filters) {
        const category = document.querySelector('#tipo-produto'), rarity = document.querySelector('#categoria');
        const price = document.querySelector('#preco'), order = document.querySelector('#ordem');
        const search = document.querySelector('.form-pesquisa input'), list = document.querySelector('.cartas');
        const cards = [...list.children], error = document.querySelector('#erro-preco');
        function readURL() {
            const params = new URLSearchParams(location.search);
            category.value = params.get('categoria') || ''; rarity.value = params.get('raridade') || '';
            price.value = params.get('preco') || ''; order.value = params.get('ordem') || ''; search.value = params.get('busca') || '';
        }
        function apply(updateURL = true) {
            const value = price.value.trim();
            const valid = value === '' || /^(?:\d+|\d{1,3}(?:\.\d{3})+)(?:,\d{1,2})?$/.test(value) || /^\d+\.\d{1,2}$/.test(value);
            if (!valid) { error.textContent = 'Informe um preço válido e positivo, como 11,50.'; price.setAttribute('aria-invalid', 'true'); price.focus(); return; }
            const grouped = /^\d{1,3}(?:\.\d{3})+$/.test(value);
            const numeric = value.includes(',') ? value.replaceAll('.', '').replace(',', '.') : grouped ? value.replaceAll('.', '') : value;
            const max = value === '' ? Infinity : Math.round(Number(numeric) * 100);
            if (!Number.isFinite(max) && value !== '') { error.textContent = 'O preço informado é muito grande.'; price.setAttribute('aria-invalid', 'true'); return; }
            price.removeAttribute('aria-invalid'); error.textContent = '';
            const query = normalize(search.value.trim());
            let count = 0;
            cards.sort((a, b) => {
                const x = byId.get(a.dataset.id), y = byId.get(b.dataset.id);
                if (order.value === 'menor-preco') return x.price - y.price;
                if (order.value === 'maior-preco') return y.price - x.price;
                if (order.value === 'nome') return x.name.localeCompare(y.name, 'pt-BR');
                if (order.value === 'lancamentos') return y.release - x.release;
                return products.indexOf(x) - products.indexOf(y);
            }).forEach(card => {
                const p = byId.get(card.dataset.id);
                const visible = (!category.value || category.value === p.category) && (!rarity.value || p.tags.includes(rarity.value)) && p.price <= max && normalize(`${p.name} ${p.description} ${p.era} ${p.category}`).includes(query);
                card.hidden = !visible; if (visible) count++; list.append(card);
            });
            document.querySelector('#resultados').textContent = `${count} produto${count === 1 ? '' : 's'} encontrado${count === 1 ? '' : 's'}${query ? ` para “${search.value.trim()}”` : ''}.`;
            document.querySelector('#sem-resultados').hidden = count !== 0;
            if (updateURL) {
                const params = new URLSearchParams();
                for (const [name, val] of [['busca', search.value.trim()], ['categoria', category.value], ['raridade', rarity.value], ['preco', value], ['ordem', order.value]]) if (val) params.set(name, val);
                history.replaceState(null, '', location.pathname + (params.size ? '?' + params : ''));
            }
        }
        filters.addEventListener('submit', event => { event.preventDefault(); apply(); });
        document.querySelector('.form-pesquisa').addEventListener('submit', event => { event.preventDefault(); apply(); });
        document.querySelector('#limpar-filtros').addEventListener('click', () => { filters.reset(); search.value = ''; apply(); });
        order.addEventListener('change', () => apply());
        window.addEventListener('popstate', () => { readURL(); apply(false); });
        readURL(); apply(false);
    }

    function renderCart() {
        const container = document.querySelector('#itens-carrinho');
        if (!container) return;
        container.replaceChildren();
        document.querySelector('#resumo-carrinho').hidden = cart.length === 0;
        if (!cart.length) {
            const message = document.createElement('p'); message.textContent = 'Seu carrinho está vazio.';
            const link = document.createElement('a'); link.href = new URL('produtos.html', root); link.className = 'btn-comprar'; link.textContent = 'Explorar produtos';
            container.append(message, link); return;
        }
        let total = 0;
        const lines = ['Olá! Gostaria de consultar a disponibilidade deste pedido:'];
        cart.forEach(item => {
            const p = byId.get(item.id); total += p.price * item.quantity;
            const row = document.createElement('article'); row.className = 'item-carrinho';
            const image = document.createElement('img'); image.src = new URL('src/img/otimizadas/' + p.image.replace(/\.(png|webp)$/, '.webp'), root); image.alt = p.name; image.width = 90; image.height = 120;
            const info = document.createElement('div');
            const title = document.createElement('a'); title.href = new URL(p.path, root); title.textContent = p.name;
            const amount = document.createElement('p'); amount.textContent = `${money(p.price)} / unidade · ${money(p.price * item.quantity)}`;
            info.append(title, amount);
            const label = document.createElement('label'); label.textContent = 'Quantidade';
            const input = document.createElement('input'); input.type = 'number'; input.min = 1; input.max = 99; input.step = 1; input.value = item.quantity; input.setAttribute('aria-label', `Quantidade de ${p.name}`);
            input.addEventListener('change', () => {
                const quantity = Number(input.value);
                if (!Number.isInteger(quantity) || quantity < 1 || quantity > 99) { input.value = item.quantity; announce('Escolha entre 1 e 99 unidades.'); return; }
                item.quantity = quantity; save(); renderCart();
                document.querySelector(`input[aria-label="Quantidade de ${p.name}"]`)?.focus();
            });
            label.append(input);
            const remove = document.createElement('button'); remove.type = 'button'; remove.textContent = 'Remover'; remove.setAttribute('aria-label', `Remover ${p.name}`);
            remove.addEventListener('click', () => { cart = cart.filter(entry => entry.id !== item.id); save(); renderCart(); announce(`${p.name} removido.`); document.querySelector('#itens-carrinho a')?.focus(); });
            row.append(image, info, label, remove); container.append(row);
            lines.push(`${item.quantity} × ${p.name} — ${money(p.price * item.quantity)}`);
        });
        document.querySelector('#total-carrinho').textContent = money(total);
        lines.push(`Subtotal: ${money(total)}`, 'Podemos combinar frete e pagamento?');
        document.querySelector('#finalizar-pedido').href = 'https://wa.me/5581988865200?text=' + encodeURIComponent(lines.join('\n'));
    }
    document.querySelector('#limpar-carrinho')?.addEventListener('click', () => { cart = []; save(); renderCart(); announce('Carrinho esvaziado.'); document.querySelector('#itens-carrinho a')?.focus(); });
    renderCart();
})();
