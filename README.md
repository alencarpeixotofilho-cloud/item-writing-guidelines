# Guia e Checklist de Elaboração de Itens

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white) ![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green?style=flat-square) ![Status](https://img.shields.io/badge/status-em%20constru%C3%A7%C3%A3o-orange?style=flat-square)

> Boas práticas para escrever e revisar itens de múltipla escolha, com checklist aplicável.

## 📌 Visão geral

Reúne as recomendações de item-writing (NBME, INEP) em um guia prático e em um checklist de revisão. Inclui exemplos de itens bem e mal construídos (todos fictícios) e um verificador automático de falhas de redação frequentes.

## ✨ Funcionalidades

- Guia de construção de enunciado, comando e alternativas
- Checklist de revisão por critérios
- Catálogo de falhas comuns (pistas, alternativas absolutas, negativas)
- Exemplos comentados (itens fictícios)
- Verificador automático de falhas de redação

## 🗂️ Estrutura do repositório

```text
checklist-elaboracao-itens/
├── guia/           # guia de elaboração (Markdown)
├── checklist/      # checklist de revisão
├── exemplos/       # itens fictícios comentados
├── src/            # verificador automático
├── LICENSE
└── README.md
```

## 🚀 Como usar

```bash
python -m src.verificar exemplos/item_exemplo.md
```

## 🔒 Dados e privacidade

Este repositório **não contém dados reais** de estudantes, docentes ou instituições.
Todos os exemplos usam **dados sintéticos** gerados pelo próprio projeto
(`exemplos/gerar_dados_exemplo`), com identificadores fictícios (`Estudante 001`, `Item 001`…).
Os itens de prova usados nos exemplos são inventados para fins de demonstração.

## 🛣️ Roadmap

- [ ] Guia de elaboração
- [ ] Checklist de revisão
- [ ] Exemplos comentados
- [ ] Verificador automático

## 📄 Licença

Distribuído sob a licença MIT. Veja [`LICENSE`](LICENSE).
