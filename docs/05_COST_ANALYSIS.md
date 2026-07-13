# Análise de Custo-Benefício — MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

## Resumo Financeiro

| Categoria | Mensal (USD) | Mensal (BRL) |
|-----------|-------------|-------------|
| Infraestrutura | $55.00 | R$ 313.50 |
| APIs Externas | $60.00 | R$ 342.00 |
| **Total Mensal** | **$115.00** | **R$ 655.50** |
| **Setup Inicial** | **$0.00** | **R$ 0.00** |

✅ **Este projeto pode começar com free tier** das ferramentas listadas.

---

## Infraestrutura & Hosting

| Serviço/Item | Mensal (USD) | Setup (USD) | Free Tier | Observações |
|--------------|-------------|------------|-----------|-------------|
| Vercel (Frontend Next.js) | $20.00 | $0.00 | ✅ Sim | Plano Pro necessário para WebSocket support e bandwidth adequado. Free tier suficiente para protótipo e staging. |
| Railway (Backend FastAPI + PostgreSQL + Celery Workers) | $25.00 | $0.00 | ✅ Sim | Plano Hobby ($5 crédito free) cobre MVP inicial. Com crescimento, plano Pro ~$25/mês para 3 serviços (API + DB + Worker). |
| Redis Upstash (Cache de Status + Broker Celery) | $10.00 | $0.00 | ✅ Sim | Free tier: 10.000 comandos/dia. Para MVP com até 500 médicos e 200 usuários, plano Pay-as-you-go ~$10/mês. |
| Supabase Storage (Fotos de médicos e assets) | $0.00 | $0.00 | ✅ Sim | Free tier: 1GB storage + 2GB bandwidth. Suficiente para fotos de perfil de médicos no MVP. |
| Sentry (Monitoramento de Erros) | $0.00 | $0.00 | ✅ Sim | Free tier: 5.000 erros/mês. Suficiente para MVP. Plano Team ($26/mês) para equipes maiores. |
| Cloudflare (CDN + DDoS Protection) | $0.00 | $0.00 | ✅ Sim | Plano Free oferece CDN global, DDoS básico e DNS gerenciado. Suficiente para o MVP. |

## APIs & Serviços Externos

| Serviço/Item | Mensal (USD) | Setup (USD) | Free Tier | Observações |
|--------------|-------------|------------|-----------|-------------|
| Anthropic Claude claude-sonnet-4-6 API (3 Agentes de IA) | $45.00 | $0.00 | ❌ Não | Estimativa para ~500 chamadas/dia (briefings diários + detecção de anomalias + predições sob demanda). Claude Sonnet: $3/MTok input, $15/MTok output. Com prompts médios de ~2K tokens, custo estimado $40-60/mês para 200 usuários ativos. |
| Google OAuth2 (Autenticação Social) | $0.00 | $0.00 | ✅ Sim | Gratuito via Google Cloud Console. Apenas configuração de OAuth2 credentials necessária. |
| Resend (Email para Magic Link / Notificações) | $0.00 | $0.00 | ✅ Sim | Free tier: 3.000 emails/mês, 100/dia. Suficiente para MVP com até 500 usuários. Plano Pro $20/mês para escalar. |
| Google Maps API (Geocoding de endereços de médicos) | $15.00 | $0.00 | ✅ Sim | $200 de crédito free/mês. Para MVP com cadastro de ~1.000 médicos e verificação de endereços, provavelmente dentro do free tier. Custos reais apenas com escala significativa. |

## Ferramentas de Desenvolvimento

| Serviço/Item | Mensal (USD) | Setup (USD) | Free Tier | Observações |
|--------------|-------------|------------|-----------|-------------|
| Desenvolvedor Full-Stack Sênior (Backend FastAPI + Arquitetura) | $3500.00 | $0.00 | ❌ Não | Estimativa para desenvolvedor sênior PJ no Brasil (~R$20.000/mês). Necessário por ~2.5 meses para Fases 1-4. |
| Desenvolvedor Frontend (Next.js + Mobile-First + PWA) | $2800.00 | $0.00 | ❌ Não | Estimativa para desenvolvedor frontend sênior PJ (~R$16.000/mês). Intensivo nas Fases 2-4. |

---

## Análise de ROI

Modelo de monetização recomendado: SaaS B2B com cobrança por laboratório/empresa. Plano Starter (até 10 propagandistas): R$499/mês. Plano Growth (até 50 propagandistas): R$1.999/mês. Plano Enterprise (ilimitado + API): R$4.999/mês. Com apenas 3 clientes no plano Growth, a receita de R$5.997/mês cobre todos os custos de infraestrutura (~R$655/mês) com margem de ~89%. Break-even financeiro (cobrindo desenvolvimento) estimado com 8-10 clientes Growth em 6 meses pós-lançamento. O principal ROI para os clientes é a redução de visitas improdutivas: se um propagandista faz 8 visitas/dia e 25% são improdutivas (médico ausente), eliminar metade dessas visitas representa ~1 hora/dia de produtividade recuperada por profissional, valendo R$500-800/mês por representante.

---

## Notas sobre Escalabilidade de Custos

- Preços baseados em uso inicial (MVP/early stage)
- Custos aumentam com volume de usuários e dados
- Reavalie a stack se atingir 10k+ usuários ativos
- Considere contratos anuais para economias de 20-40%
