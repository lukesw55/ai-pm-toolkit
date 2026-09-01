# Rubricas 1–5 — impacto e esforço

Notas verbatim do modelo Régua Comum v2. Use estas tabelas ao pontuar; o `SKILL.md` traz só o resumo.

## Dimensão 1 — ARR
*Quanto isso gera, desbloqueia, expande ou protege receita recorrente?*

| Nota | Critério | Sinais / exemplos |
|---|---|---|
| 5 | Desbloqueia ou protege ARR material em múltiplas contas; é *blocker* de deal enterprise ou de renovação relevante | IAM enterprise (SSO/SCIM) que destrava deals; tier pago do Vulnerability Manager |
| 4 | Expande receita numa faixa de contas, ou abre upsell claro, ou melhora conversão trial → paid | Upgrade Developer → Professional; enforcement de tier (free → pago) |
| 3 | Contribui indiretamente (reduz churn, melhora ativação) sem linha direta de receita | Onboarding/ativação no primeiro uso; descoberta de features |
| 2 | Receita pequena ou pontual, geralmente de uma única conta | Ajuste sob medida para fechar um deal pequeno |
| 1 | Sem efeito perceptível em receita | Pedido cosmético sem ligação com upsell ou retenção |

## Dimensão 2 — Abrangência *(inclui reutilização)*
*O problema serve a vários clientes/segmentos **E** a solução vira capability reutilizável — em vez de uma customização de uma conta só? Pergunta-chave: qual é a melhor evidência de que isso vale para mais de um cliente e vira produto reaproveitável?*

| Nota | Critério | Sinais / exemplos |
|---|---|---|
| 5 | Problema relevante para vários segmentos/prospects **e** solução vira capability de plataforma reutilizável por toda a base, sem hard-code por cliente | Evidência de CRA (todos precisam); IAM enterprise; export de relatório de vulnerabilidades para todos |
| 4 | Vários sinalizaram **e** solução reutilizável por um segmento amplo com pouca parametrização | On-prem / self-hosted edition para clientes sem cloud pública |
| 3 | Mais de uma fonte sinalizou **ou** forte hipótese de generalização; reutilizável com esforço moderado de abstração | Gestão de organização/multi-times no Cloud |
| 2 | Poucos sinais além de uma conta; reuso exigiria refazer boa parte | Integração desenhada para o fluxo interno de um cliente |
| 1 | Pedido isolado de uma única conta, hard-coded, não reaproveitável | Campo/relatório/formato de export sob medida para um único deal |

## Dimensão 3 — CRA / risco estratégico
*Isso aproxima o produto da proposta de valor ligada a segurança, evidência e compliance readiness, ou mitiga risco estratégico?*

| Nota | Critério | Sinais / exemplos |
|---|---|---|
| 5 | Central para a proposta de **CRA readiness / CRA evidence / segurança**, ou mitiga risco estratégico crítico | SBOM/VEX e relatórios audit-ready; encrypted partition / fTPM |
| 4 | Reforça claramente a narrativa de segurança / compliance readiness | Traceabilidade de CVE por dispositivo; rastreio fixado vs. em aberto |
| 3 | Tangencia segurança/compliance sem ser central | Governança de acesso (SSO/SCIM) na ótica de controle |
| 2 | Conexão fraca com segurança/estratégia | Melhoria de UX sem ângulo de segurança |
| 1 | Nenhuma relevância de CRA / segurança / estratégia | Ajuste puramente cosmético |

> **Linguagem segura:** descreva como *CRA readiness, CRA enablement, CRA evidence, CRA operational support, compliance readiness*. Não afirme que o produto "certifica compliance CRA".

## Ponderador — Confiança (desconto pela qualidade da evidência)

Em ambiente imaturo em dados, evidência qualitativa é aceitável; o que importa é quantas fontes independentes convergem.

| Confiança | Fator | Quando usar |
|---|---|---|
| **Baixa** | 0,70 | Hipótese sem validação; sinal de **uma única fonte** sem corroboração; discovery não feito |
| **Média** | 0,85 | Sinal de **2+ fontes** independentes **ou** discovery parcial; padrão coerente mas com lacunas |
| **Alta** | 1,00 | Discovery feito **+** sinais convergentes (vendas + CS + pipeline), **ou** obrigação regulatória/contratual documentada |

**Evidências qualitativas aceitáveis, por fonte:** sinais de vendas (notas de deal, win/loss, nº de oportunidades travadas) · clientes atuais (pedidos em QBR, tickets repetidos, testes de usabilidade) · CS/suporte (mesma dor entre contas) · discovery (entrevistas, surveys, protótipos) · security/CRA (texto regulatório, questionários de auditoria, prazos) · engenharia/produto (viabilidade, dívida técnica) · pipeline (nº de oportunidades dependentes).

Regra prática: **1 fonte = baixa; 2+ fontes ou discovery parcial = média; discovery + convergência ou obrigação documentada = alta.**

## Ponderador — HIPO (convicção da liderança, explícita e limitada)

| HIPO | Fator | Quando usar |
|---|---|---|
| **Despriorizar** | 0,85 | Liderança quer reduzir a prioridade (ex.: aposta estratégica saindo de foco) |
| **Neutro** | 1,00 | Padrão. Sem convicção forte — a evidência fala por si |
| **Priorizar** | 1,15 | Liderança tem convicção estratégica de elevar (ex.: "enterprise é a cunha do ano") |

**Regras de honestidade do HIPO (inegociáveis):**
1. **Padrão é Neutro.** Só sai de Neutro com decisão explícita de liderança na sala.
2. **Todo HIPO ≠ Neutro é registrado** — quem decidiu e por quê (uma frase). Sem registro, volta a Neutro.
3. **Não resgata item fraco nem mata item forte:** limitado a ±15%, move no máximo **uma faixa**. Querer mover mais é decisão **fora do modelo**, anotada como tal.
4. **Governança conta os HIPOs.** Muitos itens dependendo de HIPO = régua sendo contornada, não régua errada.

## Rubrica de esforço (Baixo / Médio / Alto)

Olhe os seis sinais; **o pior sinal puxa a nota**.

| Sinal | Baixo | Médio | Alto |
|---|---|---|---|
| Complexidade técnica | Mudança localizada, padrão conhecido | Vários componentes, algo novo | Componente novo ou problema sem solução pronta |
| Dependências | Nenhuma / só o time | 1–2 times ou um parceiro | Vários times / parceiros externos no caminho crítico |
| Risco | Baixo, reversível | Moderado | Pode quebrar fluxos existentes ou dados |
| Necessidade de discovery | Já entendido | Discovery leve | Discovery significativo antes de estimar |
| Impacto em arquitetura | Nenhum | Ajuste contido | Mexe em fundação (auth, modelo de dados, plataforma) |
| Validação / compliance | Teste padrão | Validação extra | Validação de segurança/compliance pesada |

Regra prática: **tudo Baixo = Baixo; algum Médio sem Altos = Médio; qualquer Alto = Alto.**

## Interpretação dos quadrantes

- **Prioridade máxima** (alto/baixo) — faça agora; melhor retorno por esforço.
- **Planejar** (alto/médio) — entra no próximo PI com sequenciamento e dono.
- **Avaliar trade-off** (alto/alto) — vale, mas decida o custo de oportunidade; considere fasear (MVP).
- **Quick win** (médio/baixo) — bom para preencher capacidade; agrupe vários.
- **Backlog priorizado** (médio/médio) — fila normal, sem urgência.
- **Cuidado** (médio/alto) — só com razão estratégica forte; senão adie.
- **Opportunistic** (baixo/baixo) — só se sobrar capacidade e não gerar dívida.
- **Evitar** (baixo/médio) — normalmente não compensa.
- **Não priorizar** (baixo/alto) — diga não, com clareza.
