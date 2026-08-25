# Automação de Análise de Clientes

> **Quais clientes realizaram cotações em 2025, mas não realizaram nenhuma cotação em 2026?**

## O problema

Essa foi uma demanda comercial que recebi no trabalho.

A princípio, parecia uma comparação simples entre duas planilhas. Só que, quando fui olhar os dados, percebi que não seria tão direto.

O sistema possui um limite no período de exportação. Por isso, os dados de 2025 estavam divididos em quatro arquivos e os de 2026 em outros arquivos.

Eu poderia fazer essa comparação manualmente no Excel. Inclusive, existem ferramentas que poderiam ajudar nisso.

Mas aproveitei a situação para tentar resolver o problema com programação e transformar o processo em algo que pudesse ser repetido.

## A solução

Desenvolvi um pequeno script em **Python e Pandas** que:

* lê todos os arquivos de cada ano;
* consolida os arquivos em uma única base;
* identifica os clientes pela coluna `NOME PAGADOR`;
* compara as bases de 2025 e 2026;
* identifica os clientes que cotaram em 2025, mas não aparecem em 2026;
* gera um relatório em Excel com informações para análise comercial.

O fluxo ficou basicamente assim:

```text
Arquivos de 2025
       ↓
   Consolidação
       ↓
   Base 2025
       ↓
                  Comparação
       ↑
   Base 2026
       ↑
   Consolidação
       ↑
Arquivos de 2026
       ↓
Clientes de 2025 que não cotaram em 2026
       ↓
Relatório Excel
```

Além da lista de clientes, o relatório apresenta informações como:

* quantidade de cotações em 2025;
* valor das notas fiscais;
* valor das propostas;
* frete;
* primeira cotação;
* última cotação;
* vendedor responsável.

## Tecnologias utilizadas

* **Python**
* **Pandas**
* **OpenPyXL**
* **Git**
* **GitHub**

## O resultado

A primeira versão já consegue transformar vários arquivos exportados do sistema em uma análise única.

O que antes exigiria abrir, organizar e comparar diferentes arquivos passa a seguir um fluxo reproduzível:

```text
Arquivos
   ↓
Python + Pandas
   ↓
Consolidação
   ↓
Comparação
   ↓
Relatório
```

Não é um sistema grande e nem pretende ser.

É uma solução pequena para um problema pequeno, mas um problema **real** que precisava ser resolvido.

## O que ainda pode melhorar

Hoje, a extração dos arquivos ainda é manual.

O próximo passo seria automatizar também essa parte, fazendo com que o processo evolua de:

```text
Exportar arquivos
      ↓
Executar script
      ↓
Gerar relatório
```

para algo mais próximo de:

```text
Obter dados
     ↓
Processar
     ↓
Analisar
     ↓
Gerar relatório
     ↓
Apoiar decisão comercial
```

Também seria possível adicionar uma interface, integração com ferramentas do Microsoft 365 e recursos de IA para ajudar na interpretação dos resultados.

Mas a ideia é não complicar antes da hora.

**Primeiro resolver o problema. Depois melhorar a solução.**

## Sobre os dados

Os arquivos utilizados no desenvolvimento contêm dados corporativos reais e, por isso, não estão disponíveis neste repositório.

O código disponibilizado aqui representa a estrutura e a lógica utilizadas no projeto, sem expor informações comerciais da empresa.

---

### Como esse projeto começou

Eu não comecei sabendo exatamente como resolver a demanda.

Recebi a pergunta, fui entender os dados, encontrei as limitações da extração e, a partir daí, construí uma solução simples para chegar ao resultado.

Esse projeto é justamente sobre esse processo:

**problema real → entender os dados → construir → testar → resolver → pensar na próxima melhoria.**
