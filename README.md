# Paradox TCG

Loja fictícia de cartas construída com HTML, CSS e JavaScript, sem etapa de compilação para executar. São 12 cartas e 5 produtos complementares, com páginas estáticas, busca, filtros, carrossel e carrinho.

## Executar

Na pasta do projeto, execute `python -m http.server 8000` e abra <http://localhost:8000>. Use um servidor HTTP para que o carrinho compartilhe o mesmo armazenamento entre todas as páginas.

Outra opção, sem dependências adicionais, é `node scripts/serve.cjs`, disponível em <http://127.0.0.1:8001>. Esse servidor evita cache durante o desenvolvimento.

## Funcionalidades

- Busca por nome, descrição, era e categoria, sem distinção de acentos.
- Filtros combinados de categoria, raridade e preço; aceita `11,50` e `11.50`.
- Ordenação por preço, nome e lançamentos; filtros preservados na URL.
- Carrossel manual por botões, indicadores e setas do teclado.
- Carrinho salvo em `localStorage`, quantidades de 1 a 99, remoção e subtotal.
- Link de WhatsApp prepara a mensagem do pedido. O usuário revisa e envia no WhatsApp. Não há cobrança nem envio automático. O telefone existente foi preservado e pode ser alterado em `src/js/index.js`.
- Layout adaptável, foco visível, atalho para o conteúdo, anúncios acessíveis e respeito a movimento reduzido.
- Imagens WebP otimizadas, dimensões explícitas e carregamento adiado fora das imagens principais.

## Editar conteúdo

Os dados de produtos, histórias, preços em reais e efeitos ficam em `scripts/atualizar_site.py`. As descrições foram criadas a partir das artes; os efeitos legíveis foram preservados. Os nomes originais das páginas e do catálogo foram mantidos mesmo quando diferem do título impresso na imagem.

A composição da home é mantida em `scripts/home-template.html`. Os estilos ficam em `src/css/`; `melhorias.css` reúne regras compartilhadas de acessibilidade e carrinho. A lógica de interação fica em `src/js/index.js`.

Após editar os dados ou o modelo da home, execute:

```powershell
python -m pip install Pillow
python scripts/atualizar_site.py
```

O gerador atualiza o HTML, o catálogo compartilhado `src/js/catalogo.js` e as imagens otimizadas. Não edite os arquivos gerados se pretende executar o gerador novamente. Os originais em `src/img` permanecem intactos.

Os lançamentos seguem a sequência editorial definida no catálogo. Todos os produtos, histórias e especificações comerciais são fictícios.

## Verificação

`scripts/test-site.cjs` verifica carrossel, busca, filtros, preços inválidos, carrinho, subtotal, link do pedido e as 20 páginas em larguras de 320, 375, 768, 1024 e 1440 px. Requer Playwright e Google Chrome instalado no caminho indicado no script. Com o servidor local na porta 8000 e Playwright instalado:

```powershell
node scripts/test-site.cjs
```

Para testar o servidor Node na porta 8001, defina `$env:PARADOX_URL = 'http://127.0.0.1:8001/'` antes do comando.

As capturas ficam em `qa-artifacts/`, ignorada pelo Git. Não é necessário instalar Playwright para usar o site.

## Backup

O estado anterior às melhorias está no ZIP `backups/projeto-antes-melhorias-20261027-162406.zip`, verificado após a criação. Inclui os arquivos locais do site e configurações presentes naquele momento; não inclui o histórico `.git`. A pasta de backups é ignorada pelo Git.

Para recuperar a versão anterior sem misturar os arquivos novos, extraia o ZIP em uma pasta separada e abra essa cópia.
