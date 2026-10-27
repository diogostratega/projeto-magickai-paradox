"""Gera páginas estáticas e catálogo compartilhado. Execute com Python + Pillow."""
from pathlib import Path
import json
import re
from html import escape as esc
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / 'src/img'
products = []

def card(slug, name, image, price, rarity, era, attack, defense, story, effects):
    products.append(dict(id=slug, name=name, image=image, price=round(price*100), category='cartas', rarity=rarity,
        tags=rarity.lower().split(), era=era, attack=attack, defense=defense, description=story, effects=effects,
        path=f'cartas/{slug}.html', release=len(products)))

card('juiz-solar', 'Juiz Solar Celestial', 'carta-juiz.png', 110, 'Ouro', 'Medieval', '3000', '3000',
     'Sob uma coroa de fogo, o guardião do sol pesa cada batalha perdida. Sua armadura dourada transforma a memória dos caídos em um veredito de luz.',
     ['Só pode entrar em combate quando sua Lista de Perdidos for maior que a do oponente.', 'Ganha Vantagem +3 enquanto sua Lista de Perdidos for maior que a do oponente.'])
card('juiz-negro', 'Juiz Negro Universal', 'carta-juiz-negativo.png', 333.90, 'Paradoxo', 'Medieval + Cósmico', 'X000', 'X000',
     'Do outro lado da ruptura, o juiz solar renasceu em uma armadura de cristais violetas. Ele não conta vitórias: mede a distância entre as perdas de dois mundos.',
     ['Combinação de eras: Medieval + Cósmico.', 'Sua Força e Defesa são determinadas pela diferença entre sua Lista de Perdidos e a do oponente, conforme o atributo X000 impresso na carta.'])
card('general-valente', 'General Valente', 'carta-general.png', 11.06, 'Prata', 'Medieval', '—', '2100',
     'Conhecido nos campos de batalha como General Medieval, ergue a espada sob uma chuva de flechas. Seu estandarte vermelho reúne os guerreiros que ainda resistem ao Paradoxo.',
     ['Para invocar, revele 2 criaturas Medievais de nível 1 da sua mão.', 'Ataque seu oponente: descarte 3 cartas do topo do seu deck e cause 1000 de dano para cada criatura Medieval enviada.'])
card('arqueiro-agil', 'Arqueiro Ágil', 'carta-arqueiro.png', 1.60, 'Bronze', 'Medieval', '1200', '800',
     'Entre folhas e ruínas, o arqueiro de capuz verde conhece atalhos que nenhum exército consegue seguir. Uma vitória basta para encontrar a próxima brecha na defesa inimiga.',
     ['Você pode invocar esta criatura da sua mão.', 'Após vencer uma batalha, escolha uma criatura do oponente com menos de 1000 de Defesa e envie-a para a Lista de Perdidos.'])
card('cavaleiro-medroso', 'Cavaleiro Medroso', 'carta-cavaleiro.png', 6.98, 'Bronze', 'Medieval', '1500', '500',
     'A lenda o chama de Cavaleiro Valente; os companheiros conhecem seu medo. Com a capa vermelha ao vento e a lança em punho, ele prova que coragem é voltar à batalha apesar de tudo.',
     ['Você pode invocar esta criatura da sua mão ou da Lista de Perdidos sacrificando 1 criatura Medieval.', 'Ganha +500 de Força quando invocado da Lista de Perdidos.'])
card('sacerdotisa-curandeira', 'Sacerdotisa Curandeira', 'carta-curandeira.png', 9.99, 'Bronze', 'Medieval', '800', '1200',
     'Entre as páginas do grimório e as ruínas de um antigo santuário, a sacerdotisa de cabelos rosados guarda os nomes dos caídos. Cada lembrança se torna uma nova chance de continuar.',
     ['Você pode invocar esta criatura da sua mão.', 'Quando colocada em campo, recupere 500 de HP para cada criatura Medieval na sua Lista de Perdidos.'])
card('miku-starter', 'Miku Quer Sair de Casa', 'miku-starter.png', 74.50, 'Miku Bronze', 'Origem', '500', '500',
     'A primeira versão da Miku. Emburrada, contrariada e pronta para fugir de casa para iniciar sua jornada através das eras do Paradoxo.',
     ['Você pode invocar esta criatura da sua mão ou da Lista de Perdidos se você não controlar Miku.', 'Envie esta criatura para a Lista de Perdidos: invoque 1 Miku Paradoxo.'])
card('miku-cosmica', 'Miku Sinfonia Eterna', 'miku-cosmica.png', 61.89, 'Miku Paradoxo', 'Cósmica', '2500', '2500',
     'Um microfone, uma cidade de luzes e uma plateia espalhada pelo espaço-tempo. A Miku Cósmica conduz a apresentação capaz de reunir todas as suas versões em uma única sinfonia.',
     ['Combinação: Miku + Cósmico.', 'No fim do turno, ative todos os efeitos Concerto em campo.', 'Concerto: se existirem 6 Miku de eras diferentes em campo, você vence a partida.'])
card('miku-pirata', 'Miku Cantigas de Pirata', 'miku-pirata.png', 82.37, 'Miku Paradoxo', 'Pirata', '3000', '1700',
     'De chapéu de capitã e sorriso afiado, Miku transforma o convés em palco. Entre tesouros e dados, sua tripulação navega pelas correntes imprevisíveis do Paradoxo.',
     ['Combinação: Miku + Pirata. Role 6 dados.', 'Encore: compre 1 carta e role 1 dado.', 'Concerto: compre 1 carta e role 1 dado.'])
card('miku-medieval', 'Miku Serenata Élfica', 'miku-medieval.png', 42.14, 'Miku Paradoxo', 'Medieval', '1200', '2200',
     'Nas ruínas de um reino élfico, a harpa de Miku faz florescer notas violetas. Sua serenata silencia a magia adversária e protege o último acorde dos aliados.',
     ['Combinação: Miku + Medieval. Role 1 dado.', 'Encore: todas as criaturas do oponente perdem seus efeitos.', 'Concerto: as criaturas do oponente não podem ativar efeitos ao entrar em combate.'])
card('miku-br', 'Miku Pisadinha Sambática', 'miku-br.png', 34.53, 'Miku Paradoxo', 'Brasil', '2300', '2000',
     'Vestida de verde e amarelo, Miku leva o microfone para uma festa de rua que atravessa as eras. A batida reúne versões perdidas da cantora em um palco que nunca fica vazio.',
     ['Combinação: Miku + Brasil. Role 1 dado.', 'Encore: role 1 dado; para cada ponto obtido, role mais 1 dado.', 'Concerto: pegue uma Miku da sua Lista de Perdidos para cada efeito Concerto em campo.'])
card('miku-jurassica', 'Miku Melodia Jurássica', 'miku-jurassica.png', 29.31, 'Miku Paradoxo', 'Pré-histórica', '2000', '1200',
     'Com um microfone de ossos e um dinossauro como parceiro de palco, Miku canta antes mesmo da primeira cidade existir. O ritmo selvagem fortalece todas as suas outras versões.',
     ['Combinação: Miku + Pré-histórica. Role 1 dado.', 'Encore: ganha 1 ataque extra.', 'Concerto: todas as Miku em campo ganham +500 de Força.'])

for slug,name,image,price,category,description,effects in [
 ('booster-paradoxo','Coleção Ruptura do Paradoxo','boosterbox.webp',289.90,'boosters','Uma caixa com 24 boosters para explorar criaturas e encontros entre eras. Cada abertura revela novas possibilidades para sua coleção.',['Conteúdo fictício: 24 boosters com 5 cartas cada.', 'Cartas aleatórias; as imagens ilustram a coleção.']),
 ('decks-das-eras','Decks das Eras','starter-deck.png',89.90,'decks','Um primeiro passo entre castelos e constelações. O Starter Deck reúne uma seleção pronta para aprender as mecânicas de Paradox TCG.',['Conteúdo fictício: 40 cartas, guia rápido e marcadores.', 'Edição de entrada inspirada nas eras Medieval e Cósmica.']),
 ('deckbox-paradoxo','Deckbox Portal Violeta','categorias/deckboxes.webp',39.90,'deckboxes','Guarde suas estratégias entre uma partida e outra em uma caixa inspirada nos portais do Paradoxo.',['Modelo fictício com capacidade para 80 cartas com sleeves.', 'Imagem ilustrativa da categoria.']),
 ('sleeves-paradoxo','Sleeves Ecos do Paradoxo','categorias/sleeves.webp',24.90,'sleeves','Uma camada de proteção para acompanhar suas cartas em cada nova era.',['Pacote fictício com 60 protetores de tamanho padrão.', 'Imagem ilustrativa da categoria.']),
 ('kit-marcadores','Kit de Marcadores das Eras','categorias/acessorios.webp',19.90,'acessorios','Organize o campo e acompanhe os momentos decisivos da sua partida com marcadores temáticos.',['Kit fictício com 12 marcadores e 6 dados.', 'Imagem ilustrativa da categoria.'])]:
    products.append(dict(id=slug,name=name,image=image,price=round(price*100),category=category,rarity='',tags=[],era='',attack='',defense='',description=description,effects=effects,path=f'produtos/{slug}.html',release=len(products)+1))

# As artes originais ficam preservadas; apenas as cópias de entrega são comprimidas.
optimized=IMG/'otimizadas'; optimized.mkdir(exist_ok=True)
for source in IMG.rglob('*'):
    if not source.is_file() or 'otimizadas' in source.parts or source.suffix.lower() not in ('.png','.webp'): continue
    relative=source.relative_to(IMG).with_suffix('.webp')
    target=optimized/relative; target.parent.mkdir(parents=True,exist_ok=True)
    if target.exists() and target.stat().st_mtime >= source.stat().st_mtime: continue
    with Image.open(source) as im:
        im.thumbnail((1600,1200) if source.stem=='monte-seu-deck' else (800,1100))
        im.save(target,'WEBP',quality=86,method=6)

def image_path(original): return 'src/img/otimizadas/'+str(Path(original).with_suffix('.webp')).replace('\\','/')
def image(original,prefix='',lazy=True,cls=''):
    path=image_path(original)
    with Image.open(ROOT/path) as im: w,h=im.size
    return f'<img src="{prefix}{path}" width="{w}" height="{h}" alt="{esc(cls)}" loading="{"lazy" if lazy else "eager"}" decoding="async">'
def money(cents): return ('R$ '+f'{cents/100:.2f}').replace('.',',')
def header(p=''):
    return f'''<a class="pular-conteudo" href="#conteudo">Pular para o conteúdo</a>
    <header class="cabecalho"><nav class="menu-navegacao" aria-label="Navegação principal">
    <a href="{p}index.html" class="link-logo">{image('logo-paradox.png',p,False,'Logo Paradox TCG').replace('<img ','<img class="logo" ')}</a>
    <ul class="menu"><li><a href="{p}produtos.html">Produtos</a></li><li><a href="{p}index.html#lancamentos">Lançamentos</a></li><li><a href="{p}index.html#categorias">Categorias</a></li></ul>
    <form class="form-pesquisa" action="{p}produtos.html" method="get"><input type="search" name="busca" placeholder="Pesquisar produtos" aria-label="Pesquisar produtos"><button type="submit">Pesquisar</button></form>
    <a href="{p}carrinho-de-compras.html" class="link-carrinho" aria-label="Abrir carrinho de compras">{image('carrinho.webp',p,False).replace('<img ','<img class="icone-carrinho" ')}<span class="quantidade-carrinho">0</span></a>
    </nav></header>'''
def footer(p=''):
    return f'''<footer class="rodape"><p>&copy; 2026 Paradox TCG · Universo fictício para colecionadores.</p><a href="{p}produtos.html">Explorar produtos</a></footer>
    <p id="aviso-global" class="aviso-global" role="status" aria-live="polite"></p>
    <script src="{p}src/js/catalogo.js" defer></script><script src="{p}src/js/index.js" defer></script>'''
def head(title,description,p='',extra=''):
    return f'''<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{esc(title)} | Paradox TCG</title><meta name="description" content="{esc(description,quote=True)}">
    <meta property="og:title" content="{esc(title)} | Paradox TCG"><meta property="og:description" content="{esc(description,quote=True)}"><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:image" content="{p}src/img/otimizadas/monte-seu-deck.webp"><meta name="twitter:card" content="summary_large_image">
    <link rel="icon" href="{p}src/img/otimizadas/logo-paradox.webp" type="image/webp">
    <link rel="stylesheet" href="{p}src/css/reset.css"><link rel="stylesheet" href="{p}src/css/estilos.css">{extra}<link rel="stylesheet" href="{p}src/css/melhorias.css"><link rel="stylesheet" href="{p}src/css/responsivo.css"></head>'''

for product in products:
    p='../'; effects=''.join('<p>'+esc(e)+'</p>' for e in product['effects'])
    stats=(f'<dl class="atributos"><div><dt>Era</dt><dd>{esc(product["era"])}</dd></div><div><dt>Força</dt><dd>{product["attack"]}</dd></div><div><dt>Defesa</dt><dd>{product["defense"]}</dd></div></dl>' if product['category']=='cartas' else '')
    html=head(product['name'],product['description'],p,'<link rel="stylesheet" href="../src/css/pagina-carta.css">')+f'''<body>{header(p)}<main id="conteudo" class="pagina-carta">
    <div class="imagem-carta">{image(product['image'],p,False,product['name'])}</div><div class="detalhes-carta"><a class="trilha" href="../produtos.html?categoria={product['category']}">Produtos / {product['category'].capitalize()}</a>
    <h1>{esc(product['name'])}</h1>{'<h2>Raridade: '+product['rarity']+'</h2>' if product['rarity'] else ''}
    <p class="preco-detalhe"><strong>{money(product['price'])}</strong></p><p>{esc(product['description'])}</p>{stats}
    <div class="efeito"><h3>{'Efeitos da carta' if stats else 'Conteúdo e detalhes'}</h3>{effects}</div>
    <div class="botoes"><a href="../produtos.html" class="btn-voltar">Voltar ao catálogo</a><button type="button" class="btn-comprar" data-adicionar="{product['id']}">Adicionar ao carrinho</button></div>
    <p class="nota-compra">Reúna seus produtos no carrinho e prepare o pedido pelo WhatsApp.</p></div></main>{footer(p)}</body></html>'''
    target=ROOT/product['path']; target.parent.mkdir(exist_ok=True); target.write_text(re.sub(r'>\s*<','>\n<',html),encoding='utf-8')

cards=''
for product in products:
    cards+=f'''<li class="carta" data-id="{product['id']}"><a href="{product['path']}">{image(product['image'],cls=product['name'])}</a><div class="informacoes"><h2 class="nome-personagem"><a href="{product['path']}">{esc(product['name'])}</a></h2><span class="categoria">{product['rarity'] or product['category'].capitalize()}</span><span class="preco">{money(product['price'])}</span><button class="btn-comprar" type="button" data-adicionar="{product['id']}">Adicionar ao carrinho</button></div></li>'''
category_options=''.join(f'<option value="{value}">{label}</option>' for value,label in [('cartas','Cartas avulsas'),('boosters','Boosters'),('decks','Decks iniciais'),('deckboxes','Deckboxes'),('sleeves','Sleeves'),('acessorios','Acessórios')])
html=head('Produtos e cartas','Explore cartas, boosters, decks e acessórios. Filtre por categoria, raridade e preço.',extra='<link rel="stylesheet" href="src/css/produtos.css">')+f'''<body>{header()}<main id="conteudo" class="container"><h1 class="produtos">Produtos</h1>
<form id="filtros" class="filtros"><div><label for="tipo-produto">Categoria</label><select id="tipo-produto" name="categoria"><option value="">Todas</option>{category_options}</select></div>
<div><label for="categoria">Raridade</label><select id="categoria" name="raridade"><option value="">Todas</option><option value="bronze">Bronze</option><option value="prata">Prata</option><option value="ouro">Ouro</option><option value="paradoxo">Paradoxo</option><option value="miku">Miku</option></select></div>
<div><label for="preco">Preço máximo (R$)</label><input type="text" inputmode="decimal" id="preco" name="preco" placeholder="Ex.: 11,50" aria-describedby="erro-preco"></div>
<div><label for="ordem">Ordenar por</label><select id="ordem" name="ordem"><option value="">Destaques</option><option value="lancamentos">Lançamentos</option><option value="menor-preco">Menor preço</option><option value="maior-preco">Maior preço</option><option value="nome">Nome</option></select></div>
<button type="submit" class="btn-filtrar">Aplicar filtros</button><button type="button" id="limpar-filtros" class="btn-voltar">Limpar filtros</button></form>
<p id="erro-preco" class="erro" role="alert"></p><p id="resultados" role="status" aria-live="polite"></p><p id="sem-resultados" hidden>Nenhum produto encontrado. Tente outra busca ou limpe os filtros.</p><ul class="cartas">{cards}</ul></main>{footer()}</body></html>'''
(ROOT/'produtos.html').write_text(re.sub(r'>\s*<','>\n<',html),encoding='utf-8')
(ROOT/'carrinho-de-compras.html').write_text(head('Carrinho de compras','Revise os produtos escolhidos e prepare seu pedido pelo WhatsApp.')+f'''<body>{header()}<main id="conteudo" class="container carrinho-de-compras"><h1>Carrinho de compras</h1><p>Revise sua seleção antes de preparar o pedido.</p><div id="itens-carrinho"></div><div id="resumo-carrinho" hidden><p class="total-carrinho">Subtotal: <strong id="total-carrinho"></strong></p><p>Frete, disponibilidade e pagamento serão combinados pelo WhatsApp.</p><a id="finalizar-pedido" class="btn-comprar" target="_blank" rel="noopener noreferrer">Preparar pedido no WhatsApp</a><button id="limpar-carrinho" class="btn-voltar" type="button">Esvaziar carrinho</button></div><noscript>Ative o JavaScript para gerenciar seu carrinho.</noscript></main>{footer()}</body></html>''',encoding='utf-8')

# Preserva o conteúdo e a composição da home.
home=(ROOT/'scripts/home-template.html').read_text(encoding='utf-8')
home=re.sub(r'<header.*?</header>',header(),home,flags=re.S)
home=re.sub(r'<footer.*?</footer>',lambda _:footer(),home,flags=re.S)
home=home.replace('<main>','<main id="conteudo">')
home=home.replace('<link rel="stylesheet" href="./src/css/responsivo.css">','<link rel="stylesheet" href="./src/css/melhorias.css"><link rel="stylesheet" href="./src/css/responsivo.css">')
home=home.replace('<title>Paradox TCG</title>', '<title>Paradox TCG | Cartas, decks e novas eras</title><meta name="description" content="Explore o universo fictício de Paradox TCG: cartas colecionáveis, decks, boosters e acessórios."><meta property="og:title" content="Paradox TCG"><meta property="og:description" content="Monte seu deck e domine o Paradoxo."><meta property="og:type" content="website"><meta property="og:locale" content="pt_BR"><meta property="og:image" content="src/img/otimizadas/monte-seu-deck.webp"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="src/img/otimizadas/logo-paradox.webp" type="image/webp">')
home=re.sub(r'<link rel="preconnect"[^>]*>|<link href="https://fonts.googleapis.com/[^>]*>', '',home,flags=re.S)
def optimize_tag(match):
    tag=match.group(0); found=re.search(r'src="\./src/img/(?!otimizadas/)([^"]+)"',tag)
    if not found:return tag
    original=found.group(1); path=image_path(original)
    with Image.open(ROOT/path) as im:w,h=im.size
    return tag.replace(found.group(0),f'src="{path}" width="{w}" height="{h}" loading="lazy" decoding="async"')
home=re.sub(r'<img\b[^>]*>',optimize_tag,home)
home=home.replace('href="./produtos.html?categoria=cartas" class="link-card-lancamento"','href="./cartas/miku-cosmica.html" class="link-card-lancamento"')
home=home.replace('href="./produtos.html?categoria=boosters" class="link-card-lancamento"','href="./produtos/booster-paradoxo.html" class="link-card-lancamento"').replace('href="./produtos.html?categoria=decks" class="link-card-lancamento"','href="./produtos/decks-das-eras.html" class="link-card-lancamento"')
home=home.replace('href="./produtos.html" class="botao-hero botao-principal">\n                                Comprar booster box', 'href="./produtos/booster-paradoxo.html" class="botao-hero botao-principal">\n                                Comprar booster box')
home=home.replace('href="./produtos.html" class="botao-hero botao-principal">\n                                Conhecer o Starter Deck', 'href="./produtos/decks-das-eras.html" class="botao-hero botao-principal">\n                                Conhecer o Starter Deck')
home=home.replace('href="./produtos.html" class="botao-hero botao-secundario">\n                                Ver outros decks', 'href="./produtos.html?categoria=decks" class="botao-hero botao-secundario">\n                                Ver outros decks')
(ROOT/'index.html').write_text('\n'.join(line.rstrip() for line in home.splitlines())+'\n',encoding='utf-8')
(ROOT/'src/js/catalogo.js').write_text('window.PRODUTOS = '+json.dumps(products,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print(f'{len(products)} produtos e páginas gerados.')
