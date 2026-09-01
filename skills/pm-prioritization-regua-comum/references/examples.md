# Exemplos preenchidos

Três exemplos cobrindo três quadrantes diferentes e mostrando os ponderadores em ação — inclusive o HIPO no máximo **não** resgatando uma customização (Exemplo B).

## Exemplo A — Relatório de vulnerabilidades exportável para auditoria
*(SBOM/VEX/CVE audit-ready, ligado ao Vulnerability Manager)*

| Campo | Avaliação |
|---|---|
| Origem | Security/CRA + Marketing + Discovery |
| Problema | Clientes precisam de evidência exportável e audit-ready de CVEs/SBOM/VEX para demonstrar diligência (CRA readiness) |
| Notas | D1 ARR = **4** · D2 Abrangência = **5** · D3 CRA = **5** |
| Impacto bruto | (4+5+5)/3 = **4,67** |
| Confiança | **Alta** (1,00) — regulação + múltiplas fontes |
| HIPO | **Neutro** (1,00) — a evidência se sustenta sozinha |
| Impacto final | 4,67 × 1,00 × 1,00 = **4,67 → Alto** |
| Trava alavancagem | OK (D2=5) |
| Esforço | **Médio** — reaproveita SBOM/VEX/CVE já existentes; foco em formatação + validação |
| Quadrante | Alto + Médio = **Planejar** |
| Decisão | Planejar para o próximo PI; capability central de CRA evidence, reutilizável por toda a base |

## Exemplo B — Ajuste específico pedido por um prospect para fechar um deal pequeno
*(ex.: formato de export sob medida para o ERP interno de um prospect)*

| Campo | Avaliação |
|---|---|
| Origem | Vendas (um prospect) |
| Problema | Formato de export sob medida para o ERP do prospect; vendas diz que destrava um deal pequeno |
| Notas | D1 ARR = **2** · D2 Abrangência = **1** · D3 CRA = **1** |
| Impacto bruto | (2+1+1)/3 = **1,33** |
| Confiança | **Média** (0,85) — pedido real de prospect, mas fonte única |
| HIPO | **Priorizar** (1,15) — *um líder de vendas pressiona para fechar o logo* (registrado) |
| Impacto final | min(5 ; 1,33 × 0,85 × 1,15) = **1,30 → Baixo** |
| Trava alavancagem | Dispara: D2=1 → **tratar como customização** |
| Esforço | **Baixo** |
| Quadrante | Baixo + Baixo = **Opportunistic** |
| Decisão | **Não entra como produto.** Mesmo com o HIPO no máximo, segue baixo — o modelo resiste à pressão. Caminhos: parametrizar (se houver reuso), entregar como serviço pago, ou recusar. |

## Exemplo C — Integração com ferramenta usada por vários prospects enterprise
*(IAM enterprise: SSO + SCIM, identificado como deal-blocker em discovery)*

| Campo | Avaliação |
|---|---|
| Origem | Discovery + Pipeline (vários prospects enterprise) |
| Problema | Prospects enterprise exigem SSO (autenticação) e SCIM (provisionamento) para adotar o produto em escala |
| Notas | D1 ARR = **5** · D2 Abrangência = **5** · D3 CRA = **4** |
| Impacto bruto | (5+5+4)/3 = **4,67** |
| Confiança | **Média** (0,85) — discovery feito, mas segmento/ARR ainda não confirmados |
| HIPO | **Neutro** (1,00) |
| Impacto final | 4,67 × 0,85 × 1,00 = **3,97 → Alto** |
| Trava alavancagem | OK (D2=5) |
| Esforço | **Alto** — mexe em arquitetura de identidade, modelo de organização, validação de segurança |
| Quadrante | Alto + Alto = **Avaliar trade-off** |
| Decisão | Forte candidato. **Fasear** para reduzir risco: SSO como MVP primeiro, SCIM depois. Confirmar segmento/ARR antes de comprometer todo o esforço. |
