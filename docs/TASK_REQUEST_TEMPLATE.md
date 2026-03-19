# Template de Pedido para o Assistente

Use este formato para eu ajudar mais rapido e com menos retrabalho.

## 1) Objetivo
Descreva o resultado esperado em uma frase.

Exemplo:
- Quero adicionar endpoint para cancelar consulta.

## 2) Escopo
Diga o que pode e o que nao pode mudar.

Exemplo:
- Pode alterar usecases e repositories.
- Nao pode quebrar endpoints existentes.

## 3) Criterios de Aceite
Liste como saber se ficou pronto.

Exemplo:
- Novo endpoint DELETE /consultas/<id>
- Retorno 204 em sucesso
- Retorno 404 quando consulta nao existir

## 4) Contexto Tecnico
Inclua erros, logs, payloads e comportamento atual.

Exemplo:
- Erro atual: 500 ao remover consulta de outro usuario.
- Payload de teste: {...}

## 5) Validacao Desejada
Informe como quer validar.

Exemplo:
- Teste manual com curl
- Testes automatizados com pytest

## 6) Prioridade
- Alta, Media ou Baixa
