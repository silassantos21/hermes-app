# Stack Tecnológica — MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

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

---

## Frontend

**Tecnologia Principal:** `Next.js 14 + TypeScript`

**Complementos:**
- `Tailwind CSS`
- `shadcn/ui`
- `Framer Motion`
- `React Query (TanStack)`
- `Socket.io-client`

**Justificativa:** Next.js 14 com App Router oferece performance excelente em mobile via SSR/SSG, essencial para propagandistas em campo com conexão instável. Tailwind + shadcn/ui permitem construir a interface mobile-first rapidamente com componentes acessíveis. Framer Motion para animações suaves nas notificações de XP e transições de status.

## Backend

**Tecnologia Principal:** `FastAPI (Python 3.12)`

**Complementos:**
- `SQLAlchemy 2.0`
- `Pydantic v2`
- `Celery + Redis`
- `Socket.io (python-socketio)`

**Justificativa:** FastAPI oferece performance assíncrona nativa (asyncio) fundamental para WebSockets e atualizações em tempo real com múltiplos usuários simultâneos em campo. Python facilita a integração com bibliotecas de análise de dados para detectar padrões de disponibilidade dos médicos.

## Banco de Dados

**Tecnologia Principal:** `PostgreSQL 16`

**Complementos:**
- `Prisma ORM`
- `pgvector`
- `TimescaleDB extension`

**Justificativa:** PostgreSQL suporta consultas geoespaciais (PostGIS) para localização de médicos, além de ser robusto para o histórico de reportes de status. TimescaleDB para análise temporal dos padrões de disponibilidade. pgvector para busca semântica de médicos por especialidade via embeddings.

## Autenticação & Autorização

**Tecnologia Principal:** `NextAuth.js v5`

**Complementos:**
- `JWT`
- `OAuth2 Google`
- `Magic Link via email`

**Justificativa:** Propagandistas precisam de login ágil em campo — Magic Link elimina senhas. OAuth2 com Google é padrão corporativo. JWT com refresh token garante sessões longas sem relogin durante o dia de trabalho.

## Cache & Sessão

**Tecnologia Principal:** `Redis (Upstash)`

**Complementos:**
- `React Query (TanStack)`
- `SWR`

**Justificativa:** Redis via Upstash (serverless) armazena o status atual dos médicos com TTL de 4 horas, evitando consultas repetitivas ao banco. React Query gerencia o cache no cliente com revalidação otimista, tornando os updates de status instantâneos na UI mesmo com latência de rede.

## Infraestrutura & Deploy

**Tecnologia Principal:** `Vercel (frontend) + Railway (backend)`

**Complementos:**
- `GitHub Actions CI/CD`
- `Docker`
- `Cloudflare CDN`

**Justificativa:** Vercel oferece deploy automático do Next.js com edge network global, crítico para performance mobile. Railway simplifica o deploy do FastAPI + PostgreSQL + Redis em containers Docker com escalabilidade automática. Cloudflare protege a API e serve assets estáticos próximos aos usuários no Brasil.

## Monitoramento & Observabilidade

**Tecnologia Principal:** `Sentry`

**Complementos:**
- `Vercel Analytics`
- `Grafana + Prometheus (Railway)`
- `LogRocket (replay de sessão mobile)`

**Justificativa:** Sentry captura erros críticos no frontend mobile e no backend FastAPI. LogRocket permite reproduzir sessões de usuários em campo para identificar problemas de UX. Grafana monitora latência dos WebSockets e throughput de reportes em tempo real.

## IA / Machine Learning

**Tecnologia Principal:** `Claude claude-sonnet-4-6 API`

**Complementos:**
- `LangChain`
- `Pinecone`
- `scikit-learn`

**Justificativa:** IA é usada para 3 funções: (1) Agente de Predição de Disponibilidade que analisa histórico de reportes e prevê quando um médico estará disponível, (2) Agente de Detecção de Anomalias que identifica reportes falsos ou inconsistentes para proteger a integridade dos dados, (3) Agente de Resumo Diário que gera briefings personalizados para cada propagandista com os melhores horários para visitar sua carteira de médicos.

