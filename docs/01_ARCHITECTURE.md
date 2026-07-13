# Arquitetura do Sistema — MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

## Visão Geral

O frontend Next.js 14 (Vercel) se comunica com o backend FastAPI (Railway) via REST API para operações CRUD e via WebSocket (Socket.io) para atualizações de status em tempo real. O PostgreSQL armazena o cadastro de médicos, histórico de reportes e pontuação dos usuários, enquanto o Redis (Upstash) mantém o estado atual de cada médico em cache com TTL de 4 horas. Quando um propagandista reporta um status, o evento é processado pelo FastAPI, gravado no PostgreSQL, invalidado no Redis e propagado via WebSocket para todos os usuários que estão visualizando o mesmo médico. Celery com Redis como broker executa tarefas assíncronas como calcular rankings de gamificação, enviar push notifications e acionar os agentes de IA para análise preditiva. Os agentes Claude claude-sonnet-4-6 são acionados periodicamente (cron jobs) e sob demanda para gerar predições de disponibilidade e detectar anomalias nos dados colaborativos.

## Diagrama de Arquitetura

```
CLIENTES: App Next.js (mobile browser) → VERCEL EDGE. AUTENTICAÇÃO: NextAuth.js → JWT tokens. CAMADA API: FastAPI no Railway expõe /api/v1/medicos, /api/v1/reportes, /api/v1/usuarios/pontos. WEBSOCKET: Socket.io server no FastAPI → broadcast de status updates para rooms por cidade/região. CACHE: Redis Upstash armazena status atual (key: medico:{id}:status, TTL 4h) e sessões de usuário. BANCO PRINCIPAL: PostgreSQL 16 com tabelas: medicos, reportes, usuarios, pontuacoes, historico_status. WORKERS: Celery workers no Railway processam: calcular_ranking, enviar_push_notification, acionar_agente_predicao. AGENTES IA: Claude claude-sonnet-4-6 API chamada pelo Celery para análise de padrões e geração de briefings. STORAGE: Supabase Storage para fotos de perfil de médicos e logos de laboratórios. MONITORING: Sentry SDK no frontend e backend, Grafana Dashboard monitorando WebSocket connections e reporte throughput.
```

## Componentes Principais

| Camada | Tecnologia Principal | Complementos |
|--------|---------------------|-------------|
| Frontend | `Next.js 14 + TypeScript` | `Tailwind CSS`, `shadcn/ui`, `Framer Motion`, `React Query (TanStack)` |
| Backend | `FastAPI (Python 3.12)` | `SQLAlchemy 2.0`, `Pydantic v2`, `Celery + Redis`, `Socket.io (python-socketio)` |
| Banco de Dados | `PostgreSQL 16` | `Prisma ORM`, `pgvector`, `TimescaleDB extension` |
| Autenticação | `NextAuth.js v5` | `JWT`, `OAuth2 Google`, `Magic Link via email` |
| Cache | `Redis (Upstash)` | `React Query (TanStack)`, `SWR` |
| Infraestrutura | `Vercel (frontend) + Railway (backend)` | `GitHub Actions CI/CD`, `Docker`, `Cloudflare CDN` |
| Monitoramento | `Sentry` | `Vercel Analytics`, `Grafana + Prometheus (Railway)`, `LogRocket (replay de sessão mobile)` |
| IA / ML | `Claude claude-sonnet-4-6 API` | `LangChain`, `Pinecone`, `scikit-learn` |

## Decisões Arquiteturais

As decisões foram baseadas no briefing do projeto e nas referências fornecidas.
Consulte [02_TECH_STACK.md](02_TECH_STACK.md) para justificativas detalhadas de cada escolha.

## Padrões de Projeto Recomendados

- **Frontend:** Component-driven development com Server Components (Next.js App Router)
- **Backend:** Clean Architecture (Domain → Application → Infrastructure)
- **API:** REST com versionamento (`/api/v1/`) ou tRPC para type-safety full-stack
- **Estado:** Zustand (client state) + React Query / TanStack Query (server state)
- **Testes:** Vitest (unit) + Playwright (E2E)
