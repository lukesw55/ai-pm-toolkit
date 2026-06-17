# Workshop de priorização e governança

## Como rodar um workshop (60–90 min)

**Participantes:** Product (facilita), Engineering (esforço), Sales e CS (evidência de mercado), Security (CRA/risco), liderança (HIPO, exceções, desempate). 5–7 pessoas.

**Inputs necessários (preparados antes):** lista curta de iniciativas candidatas (8–15), template em branco (ver `templates.md` ou a planilha), e a definição oficial de impacto visível na sala.

| Etapa | Tempo | O que acontece |
|---|---|---|
| 1. Enquadrar | 5 min | Ler a definição de impacto e as regras de proteção em voz alta. Lembrar: a régua é a mesma para todos. |
| 2. Evidência | 15 min | Para cada item, Sales/CS/Security trazem evidência em 1–2 frases. Sem defender notas ainda — só os fatos. |
| 3. Notas de impacto | 20–30 min | Pontuar as 3 dimensões item a item. Divergência > 1 ponto → ouvir os dois lados por 60s e fechar. Product registra. |
| 4. Ponderadores | 10 min | Definir confiança (por contagem de fontes) e HIPO (padrão Neutro; sair disso só com decisão de liderança **registrada**). Calcular impacto final. |
| 5. Trava + esforço | 10 min | Aplicar a trava de Abrangência e registrar exceções. Engineering dá o esforço (Baixo/Médio/Alto). |
| 6. Plotar e decidir | 10–15 min | Posicionar na matriz, ler o quadrante, registrar decisão e dono de cada item. |

**Output esperado:** matriz/planilha preenchida + tabela de decisões (item → quadrante → decisão → dono → próximo passo) + lista de exceções e HIPOs registrados — pronta para virar entrada do PI Planning.

Dicas: time-box cada item; o facilitador corta debates longos; nada de reabrir notas fora da etapa certa.

## Regras de proteção contra customização

- **a) Demandas de vendas** entram na régua como qualquer outra. Vendas fornece **evidência**, não a nota final. Nenhum pedido de vendas é "alto impacto" automático.
- **b) Pedidos de clientes atuais** aumentam a **confiança no problema**, não o impacto da solução. Avalie a Abrangência separadamente: "o ACME pediu" eleva confiança; só vira alto impacto se o problema se generaliza **e** a solução é reutilizável.
- **c) Trava de Abrangência (proteção principal):** nenhuma iniciativa pode ser **alto impacto** com Abrangência **baixa (1–2)**, exceto quando **obrigatória** para CRA readiness/evidence, segurança crítica, ou retenção de ARR material (deal/renovação grande comprovadamente em risco).
- **d) Exceções permitidas (override da trava):** só para os três casos de (c). Toda exceção registrada com dono, justificativa em uma frase, e o OKR/risco que protege. Sem registro, sem exceção.
- **e) HIPO não substitui a trava:** liderança pode sinalizar convicção via HIPO, mas isso **não** desliga a trava nem dispensa o registro de exceção. Item com Abrangência 1–2 elevado a Alto continua marcado como "checar exceção".
- **f) Quando tratar como customização:** se **Abrangência = 1–2 E não há exceção válida**, o item **não entra no roadmap de produto**. Três caminhos: **parametrizar** (vira config que serve a todos, e a Abrangência sobe), **entregar como serviço/projeto pago** (fora do roadmap), ou **recusar** com explicação clara.

## Governança leve

Manter o modelo vivo sem burocracia.

- **Cadência de revisão:** a cada PI/trimestre, numa retro curta de 20 min — não uma reunião nova.
- **Notas:** só recalibre uma nota antiga com evidência nova relevante (não revise o passado por esporte).
- **Thresholds (faixas):** ajuste só se, na prática, quase tudo cair na mesma faixa (a régua não separa bem).
- **Dimensões:** mude as 3 só quando os OKRs mudarem. Hoje espelham ARR, base de clientes e CRA.
- **Fatores (confiança e HIPO):** mantenha os valores por pelo menos 2 ciclos antes de mexer.
- **Monitorar o HIPO:** conte quantos itens dependeram de HIPO ≠ Neutro no ciclo. Muitos = a régua está sendo contornada; investigue por quê.
- **Monitorar exceções da trava:** se a trava é vencida com frequência, reavalie a régua.
- **Dono do modelo:** Product mantém a Régua Comum, o registro de exceções e o registro de HIPOs.
