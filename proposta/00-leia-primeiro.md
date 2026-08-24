# Proposta de redesign · agosto de 2026

Material produzido por uma equipe de 10 agentes em 19 de agosto de 2026:
diagnóstico do site atual, três direções criativas em disputa, quatro
pareceres de especialistas e a síntese de um júri.

**Nada disto está publicado.** É proposta. A decisão é do editor.

## O protótipo

Abra `prototipo-home.html` na raiz do site (funciona com duplo clique,
melhor ainda com um servidor local). Ele é autocontido: não toca em
`estilo.css`, `visual.js` nem em nenhuma página publicada.

Atalhos de demonstração por URL, além do painel flutuante:

- `prototipo-home.html?ceu=amanhecer&tema=claro`
- `prototipo-home.html?ceu=entardecer&tema=escuro`
- estados de céu: `noite`, `amanhecer`, `dia`, `entardecer` · temas: `claro`, `escuro`

## Ordem de leitura

1. `01-blueprint-final.md`, o veredito do júri e o plano de implementação.
   Se for ler um só, leia este.
2. `02-critica-do-design-atual.md`, o que preservar e o que está fraco.
3. `03-restricoes-de-performance.md`, o caderno de limites (LCP, CLS, INP, AdSense).
4. `04` a `06`, as três direções criativas completas.
5. `07` a `10`, os pareceres: WebGL/GLSL (shader pronto para a fase 2),
   motion vanilla, tipografia e o veredito tecnologia por tecnologia.

## Decisões que só o editor pode tomar

- Aprovar ou não o redesign da home (blueprint §3.1).
- As duas cores novas do modo escuro (`#0C181E` fundo, `#F0654C` chapéu),
  derivadas por necessidade de contraste. A Constituição é do editor.
- Em qual página especial o mar WebGL da fase 2 entraria, se entrar.
- O que do plano de fundação (fontes auto-hospedadas, og:image, srcset)
  vira commit primeiro.
