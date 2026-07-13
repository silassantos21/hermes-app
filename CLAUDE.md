# MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

## Contexto do Projeto

MedWaze é um aplicativo mobile-first colaborativo inspirado no Waze, voltado para propagandistas médicos. Permite que os usuários reportem em tempo real o status de atendimento e localização de médicos, acumulando pontos por contribuições (gamificação). A plataforma funciona como uma inteligência coletiva de campo para a força de vendas médica.

**Problema:** Propagandistas médicos perdem horas produtivas visitando consultórios onde o médico está ausente, atrasado ou não atende naquele dia. Não existe uma fonte de dados em tempo real e colaborativa que indique a disponibilidade dos médicos — cada profissional trabalha isoladamente, sem compartilhar informações de campo com o time.

**Público-alvo:** Propagandistas e representantes médicos de laboratórios farmacêuticos e distribuidoras de insumos médicos. Stakeholders secundários incluem gerentes distritais de vendas que precisam monitorar a produtividade da equipe de campo em tempo real.

## Stack Tecnológica

- **Frontend:** Next.js 14 + TypeScript
- **Backend:** FastAPI (Python 3.12)
- **Banco de Dados:** PostgreSQL 16
- **Infraestrutura:** Vercel (frontend) + Railway (backend)

Detalhes completos em [docs/02_TECH_STACK.md](docs/02_TECH_STACK.md).

## Estrutura do Projeto

```
medwaze-propagandistas/
├── docs/           # Planejamento e documentação
│   ├── 00_OVERVIEW.md
│   ├── 01_ARCHITECTURE.md
│   ├── 02_TECH_STACK.md
│   ├── 03_AI_AGENTS.md
│   ├── 04_TIMELINE.md
│   └── 05_COST_ANALYSIS.md
├── src/            # Código-fonte (a criar)
└── CLAUDE.md       # Este arquivo
```

## Funcionalidades Principais

- Lista de médicos com cards informativos (nome, CRM, especialidade, endereço, horário)
- Badge de status colorida em tempo real: Verde (recebendo), Amarelo (atrasado), Vermelho (indisponível)
- Painel de Ação Rápida: reportar status com 4 opções (recebendo, atrasado, não atende, endereço incorreto)
- Sistema de gamificação com pontuação XP reativa ao reportar status
- Barra de pesquisa rápida por nome ou especialidade
- Filtros rápidos: Todos, Disponíveis, Com Alertas

## Agentes de IA Disponíveis

- **AgentePredicaoDisponibilidade** — Preditor de janelas de atendimento de médicos
- **AgenteDetectorAnomalias** — Guardião da integridade dos dados colaborativos
- **AgenteBriefingDiario** — Gerador de roteiros de visita personalizados

Prompts completos em [docs/03_AI_AGENTS.md](docs/03_AI_AGENTS.md).

## Estimativa

- **Total:** 73 dias (10.4 semanas)
- **Custo Mensal:** USD 115.00 / BRL 655.50

## Arquitetura

O frontend Next.js 14 (Vercel) se comunica com o backend FastAPI (Railway) via REST API para operações CRUD e via WebSocket (Socket.io) para atualizações de status em tempo real. O PostgreSQL armazena o cadastro de médicos, histórico de reportes e pontuação dos usuários, enquanto o Redis (Upstash) mantém o estado atual de cada médico em cache com TTL de 4 horas. Quando um propagandista reporta um status, o evento é processado pelo FastAPI, gravado no PostgreSQL, invalidado no Redis e propagado via WebSocket para todos os usuários que estão visualizando o mesmo médico. Celery com Redis como broker executa tarefas assíncronas como calcular rankings de gamificação, enviar push notifications e acionar os agentes de IA para análise preditiva. Os agentes Claude claude-sonnet-4-6 são acionados periodicamente (cron jobs) e sob demanda para gerar predições de disponibilidade e detectar anomalias nos dados colaborativos.
