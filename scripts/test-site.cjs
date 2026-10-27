// Requer Playwright disponível no NODE_PATH e um servidor local na porta 8000.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.PARADOX_URL || 'http://127.0.0.1:8000/';
(async () => {
    const browser = await chromium.launch({ executablePath: 'C:/Program Files/Google/Chrome/Application/chrome.exe', headless: true });
    const page = await browser.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('requestfailed', request => console.log('Falha de rede:', request.url(), request.failure()?.errorText));
    page.on('response', response => { if (response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
    const go = file => page.goto(base + file);
    const count = () => page.locator('.carta:visible').count();
    await go('index.html');
    assert.equal(await page.locator('.slide:visible').count(), 1);
    await page.locator('.seta-proxima').click();
    assert.ok(await page.locator('.slide-lancamento').isVisible());
    await page.locator('.seta-proxima').press('ArrowRight');
    assert.ok(await page.locator('.slide-iniciante').isVisible());
    await page.locator('.indicador-slide').first().click();
    assert.ok(await page.locator('.slide-institucional').isVisible());
    await page.getByRole('searchbox').fill('serenata elfica');
    await page.locator('.form-pesquisa button').click();
    await page.waitForURL('**/produtos.html?busca=*');
    assert.equal(await count(), 1);
    await page.locator('#limpar-filtros').click();
    assert.equal(await count(), 17);
    await page.locator('#preco').fill('11,50');
    await page.locator('.btn-filtrar').click();
    assert.equal(await count(), 4);
    assert.ok(await page.locator('[data-id="general-valente"]').isVisible());
    await page.locator('#preco').fill('1.000');
    await page.locator('.btn-filtrar').click();
    assert.equal(await count(), 17);
    for (const value of ['abc', '-1', '12,345']) {
        await page.locator('#preco').fill(value); await page.locator('.btn-filtrar').click();
        assert.equal(await page.locator('#preco').getAttribute('aria-invalid'), 'true');
    }
    await page.locator('#limpar-filtros').click();
    await page.locator('#categoria').selectOption('miku');
    await page.locator('#tipo-produto').selectOption('cartas');
    await page.locator('.btn-filtrar').click();
    assert.equal(await count(), 6);
    await page.locator('#ordem').selectOption('menor-preco');
    assert.equal(await page.locator('.carta:visible').first().getAttribute('data-id'), 'miku-jurassica');
    for (const category of ['boosters', 'decks', 'deckboxes', 'sleeves', 'acessorios']) {
        await go('produtos.html?categoria=' + category); assert.equal(await count(), 1);
    }
    await go('produtos.html?busca=nada-inexistente');
    assert.equal(await count(), 0); assert.ok(await page.locator('#sem-resultados').isVisible());
    await go('cartas/miku-br.html');
    await page.locator('[data-adicionar]').click();
    await page.locator('[data-adicionar]').click();
    await page.reload(); assert.equal(await page.locator('.quantidade-carrinho').textContent(), '2');
    await page.locator('.link-carrinho').click();
    assert.match(await page.locator('#total-carrinho').textContent(), /69,06/);
    await page.locator('.item-carrinho input').fill('3');
    await page.locator('.item-carrinho input').press('Tab');
    assert.match(await page.locator('#total-carrinho').textContent(), /103,59/);
    const orderURL = new URL(await page.locator('#finalizar-pedido').getAttribute('href'));
    assert.equal(orderURL.protocol, 'https:'); assert.match(orderURL.searchParams.get('text'), /3 × Miku/);
    await page.reload(); assert.equal(await page.locator('.item-carrinho input').inputValue(), '3');
    await page.getByRole('button', { name: 'Remover Miku Pisadinha Sambática' }).click();
    assert.ok(await page.getByText('Seu carrinho está vazio.').isVisible());
    await page.evaluate(() => localStorage.setItem('paradox-carrinho-v1', '{quebrado'));
    await page.reload(); assert.ok(await page.getByText('Seu carrinho está vazio.').isVisible());
    const pages = ['index.html', 'produtos.html', 'carrinho-de-compras.html',
        ...fs.readdirSync('cartas').filter(f => f.endsWith('.html')).map(f => 'cartas/' + f),
        ...fs.readdirSync('produtos').filter(f => f.endsWith('.html')).map(f => 'produtos/' + f)];
    fs.mkdirSync('qa-artifacts', { recursive: true });
    for (const width of [320, 375, 768, 1024, 1440]) {
        console.log(`Verificando ${pages.length} páginas em ${width}px...`);
        await page.setViewportSize({ width, height: 900 });
        for (const file of pages) {
            await go(file);
            assert.ok(await page.locator('h1').count() === 1, file + ': h1');
            assert.equal(await page.locator('meta[name="description"]').count(), 1);
            assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Overflow: ${width} ${file}`);
            await page.waitForFunction(() => [...document.images].filter(i => i.loading !== 'lazy').every(i => i.complete));
            const broken = await page.locator('img').evaluateAll(imgs => imgs.filter(i => i.loading !== 'lazy' && i.naturalWidth === 0).map(i => i.src));
            assert.deepEqual(broken, [], `Imagens: ${file} ${JSON.stringify(broken)}`);
            if (file === 'index.html') {
                for (let i = 0; i < 3; i++) {
                    await page.locator('.indicador-slide').nth(i).click();
                    assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `Slide ${i}: ${width}`);
                }
            }
        }
        for (const file of ['index.html','produtos.html','cartas/miku-br.html','carrinho-de-compras.html']) {
            if (![375,1440].includes(width)) continue;
            await go(file);
            await page.evaluate(async () => {
                await document.fonts.ready;
                await Promise.all([...document.images].filter(i => i.loading !== 'lazy').map(i => i.decode().catch(() => {})));
                window.scrollTo(0, 0);
                await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
            });
            await page.screenshot({ path: path.join('qa-artifacts', `${width}-${file.replaceAll('/','-')}.png`), fullPage: true });
        }
    }
    assert.deepEqual(errors, []);
    await browser.close();
    console.log(`OK: fluxo de compra, filtros, busca, carrossel e ${pages.length} páginas em 5 larguras; sem erros de JavaScript ou HTTP.`);
})().catch(error => { console.error(error); process.exit(1); });
