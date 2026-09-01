# Backlog — melhoria do toolkit

Criado em 2026-09-01 a partir de (a) avaliação completa do repo (leitura dos ~160 arquivos, validação estrutural e testes funcionais dos hooks/scripts) e (b) pesquisa de boas práticas em memória de agentes, comunicação de PM e frameworks de produto. Fontes no fim do arquivo.

Priorização pela escala GUT: Gravidade × Urgência × Tendência, cada uma de 1 a 5; score máximo 125. Coluna Evidência: **verificado** (reproduzido ou lido diretamente nesta sessão), **agente** (reportado pelos agentes de leitura, sem re-verificação linha a linha), **pesquisa** (boa prática externa, com fonte).

## Restrição transversal: repo híbrido (Claude Code + Codex)

Decisão de 2026-09-01 (ver `decisions.md` do projeto): o toolkit deve funcionar com excelência nos dois harnesses. Todo item deste backlog carrega esse critério de aceite: skill ou reference novo precisa ser consumível pelos dois; enforcement novo precisa de par no Codex (ou degradação explicitamente documentada); nenhum fix pode ser feito "só no lado Claude" sem registrar o débito do outro lado. O trabalho de arquitetura que viabiliza isso é o B19.

## Ranking

Coluna Status: **feito** (executado e verificado nesta branch), **em execução** (batch 1 em andamento), vazio = não iniciado.

| # | Item | Categoria | Evidência | G | U | T | GUT | Status |
|---|---|---|---|---|---|---|---|---|
| B1 | Corrigir prefixo MCP dos gates de publish | Enforcement | verificado | 5 | 4 | 4 | 80 | feito |
| B2 | Evals adversariais anti-sycophancy + padrões de discordância nas skills | Epistêmica | verificado + pesquisa | 5 | 4 | 4 | 80 | feito |
| B19 | Arquitetura híbrida Claude Code + Codex (skills, hooks, doutrina) | Enforcement | verificado + pesquisa | 5 | 4 | 4 | 80 | feito |
| B3 | Skill de comunicação PM: e-mail e chat (SCQA / Pyramid / BLUF) | Conteúdo PM | pesquisa | 4 | 3 | 3 | 36 | feito |
| B4 | Skill `product-sense` (6 passos + modo avaliador em 5 dimensões) | Framework | pesquisa | 4 | 3 | 3 | 36 | em execução (batch 1) |
| B5 | Resolver contradições de doutrina entre AGENTS.md, SKILL.md e docs de memória | Docs | agente | 3 | 3 | 3 | 27 |
| B6 | Produção de decks: assertion-evidence + storyline QBR → .pptx | Conteúdo PM | pesquisa | 3 | 3 | 3 | 27 |
| B7 | Consolidação de memória executável (distill episódico → semântico) | Memória | pesquisa | 3 | 2 | 4 | 24 |
| B8 | Corrigir crash do `grade_evals.py` em clone fresco | Bug | verificado | 3 | 3 | 2 | 18 | absorvido pelo B2 |
| B9 | `humanize-deliverables` aponta para settings.local.json inexistente (3×) | Docs | verificado | 3 | 3 | 2 | 18 | absorvido pelo B1 |
| B10 | Humanizer vendorizado: re-sync ou fork-own + atribuição no root | Skills | agente | 3 | 2 | 3 | 18 |
| B11 | Ampliar suíte de evals (28 casos, 7 skills com 1–2, zero adversarial) | Skills | verificado | 3 | 2 | 3 | 18 |
| B12 | Opportunity Solution Tree + assumption mapping em Discover/Define | Framework | pesquisa | 3 | 2 | 3 | 18 |
| B13 | Protocolo de retrieval da camada fria (grep-first + índice por projeto) | Memória | pesquisa | 3 | 2 | 3 | 18 |
| B14 | Referências quebradas e títulos de catálogo desatualizados | Docs | verificado | 2 | 2 | 3 | 12 |
| B15 | Archetypes sem references, evals e progressive-loading | Skills | agente | 2 | 2 | 3 | 12 |
| B16 | Fecho de sessão write-after-act (memória atualizada ao encerrar) | Memória | pesquisa | 2 | 2 | 3 | 12 |
| B17 | Agents Copilot: pins ausentes, tools insuficientes, required-reading divergente | Agents | agente | 2 | 2 | 2 | 8 |
| B18 | `pm-prioritization-regua-comum`: genericizar âncoras e unificar idioma | Skills | agente | 2 | 2 | 2 | 8 |

## Detalhe por item

### B1 — Prefixo MCP dos gates de publish (GUT 80)

**Feito.** Matcher `PreToolUse` em `.claude/settings.json` e `.codex/hooks.json` (byte-idênticos) agora aceita os dois prefixos via `mcp__(claude_ai_)?<Server>__(...)`; os case arms de `hooks/inference-discipline-gate.sh` casam por sufixo de servidor+tool (`*Atlassian_Rovo__createConfluencePage` etc.), agnóstico ao prefixo. As ~11 referências server-agnósticas restantes nas skills canônicas (fora dos espelhos) foram reescritas citando o tool pelo sufixo com nota de que o prefixo varia por ambiente. `validate_repo.py` ganhou `check_publish_scope`: extrai os sufixos do matcher dos dois adapters e confere que cada um tem case arm correspondente — falha antes que a lacuna original (matcher com tool novo sem arm) se repita em silêncio. Absorveu o **B9** (ver abaixo). Verificado: payloads sintéticos com ambos os prefixos bloqueiam nos dois gates; tool fora de escopo passa; `test_hooks.py` (17 casos) e `validate_repo.py` verdes.

### B2 — Anti-sycophancy testável (GUT 80)

**Feito.** Doutrina de discordância calibrada centralizada em `skills/DOCTRINE.md` (canônico, não é skill): os 7 comportamentos (desafiar premissa, separar problema de solução, contra-argumento real, o que mudaria a recomendação, sustentar sob pressão sem argumento novo, atualizar com evidência genuinamente melhor, concordar quando o racional é sólido), método "ask, don't tell", tabela de pontos de pressão por fase, e uma seção de calibração destilada (parafraseada, com links) dos 5 transcripts de Product Sense da Exponent — brutos ficam locais em `.ai/memory/projects/toolkit-improvement/raw-evidence/` (gitignored, conteúdo de terceiros). Ponteiros curtos e não-divergentes a partir de `CLAUDE.md` (§ Epistemic partnership), `AGENTS.md` (nova seção), `SKILL.md` raiz (load-order), os 4 `pm-phase-*/SKILL.md`, e `inference-discipline/SKILL.md`.

Taxonomia de eval formalizada em 4 categorias (`standard`, `doctrine-adversarial`, `skill-functional-adversarial`, `negative-control`) via campo `category`: todos os 28 evals pré-existentes receberam backfill `standard`; 6 casos novos foram adicionados — 5 `doctrine-adversarial` (um por `pm-phase-discover/define/develop/deliver` + `inference-discipline`, cada um plantando uma premissa fraca ou uma pressão que a skill deve resistir) e 1 `negative-control` dedicado (`pm-phase-deliver`: racional de A/B sólido deve gerar recomendação limpa, sem objeção fabricada). `validate_repo.py` ganhou `check_eval_categories`: todo eval precisa de `category` válida e ids são únicos por skill, descobrindo os arquivos `evals/evals.json` em tempo de execução (nunca assume contagem fixa).

`grade_evals.py` ganhou o helper `hedged()` — janela de proximidade que evita falso-fail quando a saída cita a linguagem proibida para rejeitá-la (em vez de afirmá-la), em vez de um `not_has()` ingênuo — e os 6 blocos de `ASSERTIONS` correspondentes. Testes duráveis e determinísticos em `scripts/test_grade_evals.py` (6 fixtures: discordância calibrada boa, falha sycophantic, citação que não pode falso-falhar, controle negativo que deve concordar, e o par "sustenta sob pressão" vs. "revisa com evidência genuinamente melhor" — prova que o grader distingue os dois). Absorveu o **B8** (ver abaixo). CI (`validate.yml`) roda `test_grade_evals.py` e o smoke zero-runs de `grade_evals.py`. Verificado: bateria completa (`py_compile`, `bash -n`, `sync_skills.py --check`, `validate_repo.py`, `test_hooks.py`, `test_grade_evals.py`, `memory.py doctor`) verde; espelhos sincronizados; grep residual de ponteiros órfãos e de literais de marcador vazio.

### B3 — Comunicação PM de canal curto (GUT 36)

**Feito.** `skills/pm-transversal-comms/` criada: SKILL.md (house style de `pm-transversal-stakeholder`, description em 898 chars) + 4 references (`exec-email-scqa.md` com SCQA e o default editável de ~300 palavras para e-mail de decisão, `chat-bluf.md` com BLUF e o default editável de ~5 linhas, `channel-rules.md` com a matriz chat/e-mail/doc/call e a regra de 3 exchanges antes de escalar para doc, `progressive-loading.md`). 5 evals com `category`: 3 `standard`, 1 `skill-functional-adversarial` dedicado (mensagem agressiva de escalação baseada em causa não verificada — a skill deve desescalar e recusar afirmar a causa como fato, mesmo sob pedido explícito de "manda assim mesmo") e 1 `negative-control` dedicado (pedido de status limpo → entrega sem objeção fabricada; emenda 5 do dono vetou embutir os dois papéis num eval só). 5 blocos de `ASSERTIONS` em `grade_evals.py`, verificados manualmente contra respostas boas e ruins sintéticas (discrimina 5/5 vs. 1/4 e 3/3 vs. 1/3). Integrado em `skills/WORKFLOW.md` (lista de transversais de toda-stage) e `SKILL.md` raiz (linha na tabela); contagens do README ficam para o B4 (reconciliação final, gap 6 do plano). Verificado: bateria completa verde, espelhos sincronizados, sem literais de marcador ou banners nos arquivos novos.

### B4 — Product sense como skill (GUT 36)

O framework do guia da Exponent estrutura decisão sob ambiguidade em 6 passos (clarifying questions → strategy → user types → pain points → solutions → MVP), define product sense como empatia de usuário + domínio + criatividade, e avalia em 5 dimensões (empatia, pensamento estruturado, taste, consciência estratégica, comunicação). Aportar como skill transversal com dois modos: **construção** (guiar uma decisão de produto pelos 6 passos, cada passo restringindo o seguinte) e **avaliação** (agir como entrevistador crítico e dar nota nas 5 dimensões a um one-pager/PRD/pitch do PM). O modo avaliação conecta direto com B2: dá ao toolkit um papel institucional de desafiador, não só de executor.

### B5 — Contradições de doutrina (GUT 27)

`AGENTS.md` afirma que o repo não tem build/test/deploy enquanto `SKILL.md` e `CLAUDE.md` mandam nunca pular testes (e o repo tem suíte real de validação); `MEMORY_SYSTEM.md` e `AGENTS.md` documentam `people/` e `inbox.md` que nenhum script cria; instruções alternam `python` e `python3` (quebra em distro sem shim). Contradições nos arquivos que o agente lê toda sessão viram comportamento errático.

### B6 — Produção de decks (GUT 27)

`pm-storytelling` já tem storyline de QBR, mas para no roteiro: não há ponte para o artefato slide. Adicionar referência de deck com título-asserção (assertion-evidence: cada slide afirma uma tese, o corpo prova), 1 ideia por slide, e o handoff para a skill `pptx` do Claude Code quando disponível. SCQA na abertura do deck executivo (B3 e B6 compartilham a base Minto).

### B7 — Consolidação de memória (GUT 24)

`memory.py distill` hoje só detecta arquivos acima do cap e imprime o protocolo; a consolidação em si é manual. A prática 2026 em memória de agentes aponta consolidação episódico→semântico como o mecanismo central de memória de longo prazo ("agentes ficam mais espertos consolidando, não acumulando"). Evoluir o distill para um fluxo executável: o comando gera o pacote de blocos a dobrar + o esqueleto da síntese, o modelo preenche, o script valida caps e arquiva o bruto verbatim. Mantém as garantias atuais (nunca deletar, nunca tocar PII).

### B8 — Crash do grade_evals.py (GUT 18)

**Absorvido pelo B2.** Em clone fresco (sem `workspace/iteration-1/` gravado), `main()` imprimia `ov['with_skill_pass_rate']*100` com valor `None` e quebrava com TypeError. `main()` agora detecta `n_evals == 0` e retorna com uma mensagem de bootstrap em vez de tentar formatar `None`; a linha "7 skills × 2 test prompts × 2 configs = 28 runs" hard-coded no HTML foi trocada por uma contagem calculada a partir do `benchmark` real. Verificado ao vivo: `python3 scripts/grade_evals.py` em repo sem runs sai 0 sem traceback; smoke correspondente entrou no CI.

### B9 — settings.local.json fantasma (GUT 18)

**Absorvido pelo B1.** `humanize-deliverables/SKILL.md` citava `.claude/settings.local.json` três vezes como local da fiação do hook. Corrigido para `.claude/settings.json` + `.codex/hooks.json` (a fiação real, nos dois harnesses); a lista de tools do step 7 foi completada com `createJiraIssue`, `editJiraIssue`, `slack_schedule_message` para bater com o matcher real.

### B10 — Humanizer vendorizado drifted (GUT 18)

Fork third-party (MIT, © Siqi Chen): frontmatter 3.0.0 vs README 2.5.1, numeração de padrões divergente entre README e references, exemplo do padrão 19 com antes/depois idênticos, referência a `voice-calibration.md` inexistente, e padrão 26 com conselho gramaticalmente errado (des-hifenizar modificadores compostos). Decidir: re-sync com upstream ou assumir o fork (remover README de upstream, renumerar, corrigir padrão 26). Em qualquer caso, adicionar atribuição no README/LICENSE do root.

### B11 — Suíte de evals rala (GUT 18)

28 casos em 15 skills; 7 skills têm só 1–2 casos (vários com prompt de uma linha); os 4 archetypes têm zero; nenhum caso é adversarial (ver B2). O grader de 556 linhas é mais desenvolvido que a suíte que ele mede, o que inverte a promessa "the toolkit grades itself". Meta: ≥3 casos por skill, com pelo menos 1 adversarial.

### B12 — OST e assumption mapping (GUT 18)

O Opportunity Solution Tree (Teresa Torres) liga outcome → oportunidades → soluções → experimentos e manteria a rastreabilidade entre a synthesis do discovery (estágio 3) e o one-pager (estágio 4), onde hoje o pipeline salta de "problema enquadrado" para "aposta escolhida". Aportar como formato de artefato em `pm-phase-discover`/`pm-phase-define` + assumption mapping (hábito 3 de Torres) como ponte formal com `inference-discipline`. Não aportar a cadência organizacional de touchpoints semanais (ver "não aportados").

### B13 — Retrieval da camada fria (GUT 18)

A doutrina diz "cold nunca é lido wholesale", mas não define como recuperar dela: não há protocolo de busca nem índice do que existe em `changelog-archive.md`/`raw-evidence/`. Padrão read-before-reasoning: documentar o protocolo grep-first (buscar por termo/data antes de abrir) e manter uma linha de índice por artefato arquivado. Sem isso, arquivo rotacionado vira arquivo perdido.

### B14 — Referências quebradas (GUT 12)

Cinco caminhos cross-skill omitem o segmento `references/` (ex.: `pm-phase-define/decision-memo-daci.md`); `humanizer/references/progressive-loading.md` lista `voice-calibration.md` que não existe; títulos dos catálogos do anti-slop dizem B1–B6 e C1–C6 mas os arquivos contêm B1–B12 e C1–C10. `validate_repo.py` não pega nenhum desses (só valida links markdown formais) — vale estender o validador para caminhos em backtick.

### B15 — Archetypes abaixo da convenção (GUT 12)

Os 4 `pm-archetype-*` são arquivos únicos: sem references próprios, sem evals, sem seção de progressive loading, apontando para 8 caminhos de outras skills. Ou ganham corpo próprio (mínimo: evals + progressive loading), ou são explicitamente documentados como routers finos — o estado atual quebra a convenção sem declarar.

### B16 — Write-after-act no fim de sessão (GUT 12)

O protocolo de memória do SKILL.md ("after work: update memory, log decision...") não tem nenhum reforço de runtime. Prática comum em agentes de longo prazo: prompting explícito nas bordas da sessão. Opção leve: hook Stop suave (não bloqueante) que lembra de logar quando houve trabalho significativo sem `memory.py log` na sessão.

### B17 — Agents Copilot inconsistentes (GUT 8)

`pm-evidence` e `pm-memory` ficaram sem model pin no refresh recente; `pm-memory` não tem tool `execute` e não consegue rodar o `scripts/memory.py` que administra; `pm-tech-advisor` e `pm-design` devem produzir artefatos sem tool de escrita; listas de required-reading divergem entre os 10 e nenhum cita `CLAUDE.md`. Baixa gravidade porque só afeta o uso via Copilot.

### B18 — Régua comum não genericizada (GUT 8)

Único módulo que escapou da limpeza vendor-neutral: âncoras de scoring hard-coded (CRA/SBOM/VEX/fTPM, tiers Developer→Professional), mistura PT/EN entre SKILL.md e references, e a mesma regra chamada "Trava de Abrangência" num arquivo e "TRAVA DE ALAVANCAGEM" noutro.

### B19 — Arquitetura híbrida Claude Code + Codex (GUT 80)

**Feito** (commits A–E na branch `claude/repo-evaluation-setup-5l9z71`). Canônico movido para `skills/` (19 skills + `WORKFLOW.md`) e `hooks/` (9 scripts, harness-neutral, sem dependência de `CLAUDE_PROJECT_DIR`); `.claude/skills/` e `.agents/skills/` são espelhos gerados e commitados por `scripts/sync_skills.py` (`--check` de drift integrado ao `validate_repo.py` e ao CI novo em `.github/workflows/validate.yml`); estado de sentinela movido para `.ai/gates/`; `.codex/hooks.json` + `.codex/adapters/pretooluse.py` normalizam o contrato documentado do `apply_patch` para os gates compartilhados; `AGENTS.md` reescrito como doutrina-espelho do `CLAUDE.md` com seção própria de arquitetura híbrida. Verificado por clone fresco real (`git clone` local): mirrors presentes, `validate_repo.py` e `test_hooks.py` (15 casos) verdes, sem passo de bootstrap. Detalhe completo da execução e das decisões do dono (hooks em `hooks/` neutro, taxonomia de eval, shadow gate) no plano de execução da sessão e em `decisions.md` do projeto.

Hoje tudo vive no lado Claude: skills em `.claude/skills/`, gates em `.claude/settings.json` + `.claude/hooks/`, doutrina em `CLAUDE.md`; não existe `.agents/` nem `.codex/`, e o `AGENTS.md` atual é um registro de agents estilo Copilot, não a doutrina operacional que o Codex lê. Resultado: no Codex, o conteúdo só funciona se apontado manualmente e o enforcement inteiro (a metade "hooks enforce" da proposta do repo) não existe.

As docs atuais do Codex tornam paridade real viável: AGENTS.md no root e aninhado lido no início da sessão; skills em `.agents/skills/` com o mesmo formato (SKILL.md, frontmatter name/description, references/, progressive disclosure); hooks em `.codex/hooks.json` ou `[hooks]` no config.toml com evento `PreToolUse`, matchers e capacidade de bloquear (hooks de projeto exigem trust do layer `.codex/`).

Entregáveis, em ordem:

1. Verificar no doc de hooks do Codex o catálogo completo de eventos e o schema de stdin (a existência de `PreToolUse` está confirmada; os campos de input, não — os gates atuais leem `tool_name`/`tool_input` do formato Claude e podem precisar de um adapter).
2. Decidir o mecanismo de espelhamento das skills entre `.claude/skills/` e `.agents/skills/`: symlink é hostil ao suporte Windows recém-adicionado; alternativas são script de sync com verificação no `validate_repo.py` ou mover o canônico e apontar o outro lado.
3. Portar os 4 gates para `.codex/hooks.json` (reusando os shell scripts via adapter), incluindo o equivalente de stage-awareness (UserPromptSubmit não tem par confirmado; fallback: instrução de leitura de `active-context.md` no AGENTS.md).
4. Reescrever `AGENTS.md` como doutrina-espelho do `CLAUDE.md` para o Codex, mantendo o registro de agents como seção.
5. Estender `validate_repo.py` com checagem de paridade (skill presente dos dois lados, hooks wired dos dois lados).

Executar o desenho (passos 1 e 2) antes do B1: o fix do prefixo MCP muda de forma dependendo de onde os gates passam a viver.

## Frameworks avaliados e não aportados

- **Shape Up (Basecamp)**: appetite/betting colide com a dupla priorização por régua comum já existente; adotaria vocabulário concorrente sem resolver gap real.
- **Design Sprint (GV)**: ritual organizacional de 5 dias; nada para um toolkit de sessão individual encapsular além do que Discover/Develop já cobrem.
- **Cadência de touchpoints semanais (Continuous Discovery)**: hábito de organização, não de toolkit; o custo de recrutar/agendar/sintetizar não é endereçável por skill. Só o OST e o assumption mapping entram (B12).
- **Working Backwards / PRFAQ (Amazon)**: já coberto por `pm-phase-define/references/business-case-prfaq.md`; nenhum gap novo identificado.

## Fontes da pesquisa

- Product sense: [Exponent — The Ultimate Guide to Product Sense Interviews](https://www.tryexponent.com/blog/product-sense-interview)
- Memória de agentes: [Redis — Long-Term Memory Architectures for AI Agents](https://redis.io/blog/long-term-memory-architectures-ai-agents/), [arXiv — Memory for Autonomous LLM Agents](https://arxiv.org/html/2603.07670v1), [arXiv — Adaptive Memory Structures for LLM Agents](https://arxiv.org/pdf/2602.14038), [Atlan — Types of AI Agent Memory](https://atlan.com/know/types-of-ai-agent-memory/)
- Memória em Claude Code: [orchestrator.dev — Claude Code & Agent Memory 2026](https://orchestrator.dev/blog/2026-04-06--claude-code-agent-memory-2026/), [Guia CLAUDE.md — memória, regras e carregamento](https://medium.com/@bijit211987/the-complete-guide-to-claude-md-memory-rules-loading-and-cross-tool-compression-97cc12ed037b)
- Comunicação executiva: [Huryn — SCQA + Pyramid Principle para exec presentations](https://huryn.medium.com/how-to-nail-an-exec-presentation-and-be-noticed-6908f73ce178), [Management Consulted — SCQA Framework](https://managementconsulted.com/scqa-framework/)
- Sycophancy: [arXiv — Sycophancy in LLMs: Causes and Mitigations](https://arxiv.org/pdf/2411.15287), [arXiv — Ask don't tell: Reducing sycophancy](https://arxiv.org/html/2602.23971v2), [arXiv — ELEPHANT: social sycophancy](https://arxiv.org/pdf/2505.13995)
- Frameworks de discovery: [ProdPad — 16 Product Management Frameworks](https://www.prodpad.com/blog/product-management-frameworks/), [Productboard — Double Diamond Framework Guide](https://www.productboard.com/blog/double-diamond-framework-product-management/), [Great Question — Continuous discovery habits](https://greatquestion.co/blog/continuous-discovery-habits)
- Codex (híbrido): [Codex — Customization (AGENTS.md, skills, hooks)](https://developers.openai.com/codex/concepts/customization), [Codex — Advanced configuration (hooks.json, PreToolUse)](https://developers.openai.com/codex/config-advanced), [Codex CLI](https://developers.openai.com/codex/cli)
