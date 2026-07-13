# Cronograma do Projeto — MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

## Resumo

| # | Fase | Duração |
|---|------|---------|
| 1 | Fase 0 — Prototipagem e Validação (HTML/React Estático) | 7 dias |
| 2 | Fase 1 — Setup de Infraestrutura e Autenticação | 10 dias |
| 3 | Fase 2 — Core Features: Lista de Médicos e Reportes | 21 dias |
| 4 | Fase 3 — Gamificação Avançada e Agentes de IA | 21 dias |
| 5 | Fase 4 — Polimento, Testes e Lançamento Beta | 14 dias |
| | **Total** | **73 dias (10.4 semanas)** |

---

## Detalhamento das Fases

### Fase 1: Fase 0 — Prototipagem e Validação (HTML/React Estático) (7 dias)

#### Tarefas

- [ ] Construir protótipo funcional em HTML único com React + Tailwind (conforme especificação do briefing)
- [ ] Implementar todos os 4 médicos de dados mockados (medicosIniciais)
- [ ] Criar sistema de badges coloridas e filtros rápidos (Todos/Disponíveis/Com Alertas)
- [ ] Implementar Painel de Ação Rápida com menu de reporte de status
- [ ] Adicionar lógica reativa de gamificação (contador XP no header)
- [ ] Barra de pesquisa funcional por nome e especialidade
- [ ] Notificações de sucesso com XP ganho
- [ ] Testes de usabilidade com 3-5 propagandistas reais para validar o fluxo

#### Entregáveis

- Arquivo index.html funcional com protótipo completo do MedWaze
- Relatório de feedback dos testes de usabilidade com propagandistas
- Decisão go/no-go para desenvolvimento full-stack

---

### Fase 2: Fase 1 — Setup de Infraestrutura e Autenticação (10 dias)

#### Tarefas

- [ ] Setup do monorepo (Next.js 14 + FastAPI) com Docker Compose local
- [ ] Configurar PostgreSQL com schema inicial (tabelas: usuarios, medicos, reportes, pontuacoes)
- [ ] Configurar Redis Upstash para cache de status
- [ ] Implementar NextAuth.js com Magic Link e OAuth2 Google
- [ ] Deploy inicial no Vercel (frontend) e Railway (backend)
- [ ] Configurar GitHub Actions para CI/CD com testes automáticos
- [ ] Configurar Sentry para monitoramento de erros
- [ ] Seed do banco com dados de médicos reais (CRM/especialidade/endereço)

#### Entregáveis

- Ambiente de desenvolvimento local funcionando com Docker Compose
- Pipeline CI/CD configurado e deployando em staging
- Sistema de autenticação funcional com Magic Link
- Schema de banco de dados documentado e versionado

---

### Fase 3: Fase 2 — Core Features: Lista de Médicos e Reportes (21 dias)

#### Tarefas

- [ ] API REST FastAPI: CRUD de médicos com paginação e busca full-text
- [ ] API de reportes: endpoint POST /reportes com validação Pydantic e cálculo de XP
- [ ] Implementar WebSocket (Socket.io) para broadcast de status em tempo real
- [ ] Frontend: tela principal mobile-first com lista de médicos e cards
- [ ] Frontend: componente de badge de status com animação Framer Motion
- [ ] Frontend: Painel de Ação Rápida com menu bottom sheet (mobile-native UX)
- [ ] Frontend: integração WebSocket com React Query para updates otimistas
- [ ] Sistema de filtros (Todos/Disponíveis/Com Alertas) com React Query
- [ ] Barra de pesquisa com debounce e busca no backend
- [ ] Lógica de gamificação: acúmulo de XP, histórico de pontos por usuário
- [ ] Tela de perfil do usuário com total de XP e histórico de contribuições
- [ ] Testes de carga nos WebSockets com 100 usuários simultâneos

#### Entregáveis

- Aplicação full-stack funcional com lista de médicos em tempo real
- Sistema de reporte de status com gamificação funcionando
- WebSocket estável com latência < 500ms para atualizações de status
- Suite de testes (Jest + Pytest) cobrindo fluxo principal de reporte

---

### Fase 4: Fase 3 — Gamificação Avançada e Agentes de IA (21 dias)

#### Tarefas

- [ ] Implementar ranking semanal/mensal de propagandistas por XP
- [ ] Sistema de conquistas (badges): 'Primeiro Reporte', 'Contribuidor do Mês', '100 Reportes'
- [ ] Integrar Claude claude-sonnet-4-6 API para AgentePredicaoDisponibilidade
- [ ] Implementar AgenteDetectorAnomalias com Celery worker
- [ ] Cron job diário às 06:00 para AgenteBriefingDiario
- [ ] Tela de 'Insights do Médico' mostrando predição de disponibilidade
- [ ] Implementar push notifications via PWA (Service Worker) para briefing diário
- [ ] Dashboard gerencial para líderes distritais: mapa de calor de disponibilidade
- [ ] Exportação de relatório CSV/PDF de visitas e status por região

#### Entregáveis

- Sistema de ranking e conquistas funcionando
- 3 agentes de IA integrados e funcionando em produção
- PWA configurada com push notifications
- Dashboard gerencial básico para gestores

---

### Fase 5: Fase 4 — Polimento, Testes e Lançamento Beta (14 dias)

#### Tarefas

- [ ] Testes de usabilidade com grupo de 10-20 propagandistas em campo
- [ ] Correção de bugs e ajustes de UX baseados no feedback
- [ ] Otimização de performance: Lighthouse score > 90 em mobile
- [ ] Implementar modo offline (PWA cache) para uso sem internet
- [ ] Auditoria de segurança (OWASP Top 10) e proteção de dados de médicos (LGPD)
- [ ] Documentação da API com Swagger automático do FastAPI
- [ ] Configurar monitoramento de uptime e alertas de incidente
- [ ] Onboarding in-app com tutorial guiado para novos usuários
- [ ] Lançamento beta fechado com 1 laboratório parceiro

#### Entregáveis

- Aplicação com Lighthouse score > 90 em mobile
- Modo offline funcional para consulta de médicos sem internet
- Relatório de auditoria de segurança e conformidade LGPD
- Beta lançado com primeiro laboratório parceiro
- Documentação técnica completa

---

## Premissas

- Time de desenvolvimento: 1 desenvolvedor full-stack sênior + 1 desenvolvedor mobile/frontend
- O protótipo HTML da Fase 0 será validado com usuários reais antes de iniciar a Fase 1
- Dados de médicos (CRM, endereço, especialidade) serão fornecidos pelo cliente em planilha — sem necessidade de integração com CRM médico externo no MVP
- A infraestrutura opera dentro dos limites do free tier na Fase 0-1, custos reais começam na Fase 2
- Notificações push funcionam via PWA (sem necessidade de app nativo iOS/Android no MVP)
- Não há integração com sistemas de CRM de laboratórios farmacêuticos no MVP — dados são inseridos manualmente
- Chaves de API da Anthropic (Claude) disponíveis antes do início da Fase 3
