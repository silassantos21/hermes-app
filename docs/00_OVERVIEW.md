# MedWaze — Plataforma Colaborativa de Status de Médicos para Propagandistas

> MedWaze é um aplicativo mobile-first colaborativo inspirado no Waze, voltado para propagandistas médicos. Permite que os usuários reportem em tempo real o status de atendimento e localização de médicos, acumulando pontos por contribuições (gamificação). A plataforma funciona como uma inteligência coletiva de campo para a força de vendas médica.

**Tipo de Projeto:** `saas`
**Gerado em:** 24/06/2026 13:33
**Estimativa Total:** 73 dias (10.4 semanas)
**Custo Mensal Estimado:** USD 115.00 / BRL 655.50

---

## Problema que Resolve

Propagandistas médicos perdem horas produtivas visitando consultórios onde o médico está ausente, atrasado ou não atende naquele dia. Não existe uma fonte de dados em tempo real e colaborativa que indique a disponibilidade dos médicos — cada profissional trabalha isoladamente, sem compartilhar informações de campo com o time.

## Público-Alvo

Propagandistas e representantes médicos de laboratórios farmacêuticos e distribuidoras de insumos médicos. Stakeholders secundários incluem gerentes distritais de vendas que precisam monitorar a produtividade da equipe de campo em tempo real.

## Funcionalidades Principais

- Lista de médicos com cards informativos (nome, CRM, especialidade, endereço, horário)
- Badge de status colorida em tempo real: Verde (recebendo), Amarelo (atrasado), Vermelho (indisponível)
- Painel de Ação Rápida: reportar status com 4 opções (recebendo, atrasado, não atende, endereço incorreto)
- Sistema de gamificação com pontuação XP reativa ao reportar status
- Barra de pesquisa rápida por nome ou especialidade
- Filtros rápidos: Todos, Disponíveis, Com Alertas
- Notificação de sucesso com XP ganho ao reportar
- Feed de atualizações recentes da comunidade

## Diferenciais

- Modelo colaborativo estilo Waze aplicado ao contexto de saúde e força de vendas médica — pioneiro no Brasil
- Gamificação com XP e ranking que incentiva ativamente a contribuição da equipe de campo
- Atualização de status em tempo real via WebSocket, sem necessidade de recarregar a página
- Dados enriquecidos por IA que detectam padrões de disponibilidade por médico, dia da semana e horário

## Escopo do MVP (Mínimo Produto Viável)

- [ ] Protótipo HTML/React funcional com dados mockados (Fase 0) — entregável imediato
- [ ] Cadastro e listagem de médicos com cards informativos (nome, CRM, especialidade, endereço, horário)
- [ ] Sistema de badges de status: Verde/Amarelo/Vermelho com atualização em tempo real via WebSocket
- [ ] Painel de Ação Rápida com 4 opções de reporte (recebendo, atrasado, não atende, endereço incorreto)
- [ ] Gamificação básica: acúmulo de XP por reporte e exibição do total no header
- [ ] Filtros rápidos: Todos / Disponíveis / Com Alertas
- [ ] Barra de pesquisa por nome e especialidade com debounce
- [ ] Autenticação via Magic Link (email) para acesso rápido em campo
- [ ] PWA básica para instalação no celular sem app store
- [ ] Notificação de sucesso com XP ganho ao reportar status

## Funcionalidades Futuras (v2+)

- Mapa interativo (Google Maps/Mapbox) com pins coloridos mostrando status dos médicos por região
- Integração com CRMs farmacêuticos (Salesforce Health Cloud, IQVIA)
- App nativo iOS e Android com React Native para notificações push nativas
- Ranking gamificado com leaderboard regional e nacional de propagandistas
- Sistema de conquistas (badges) e recompensas resgatáveis (vouchers, benefícios)
- Dashboard gerencial avançado com heatmap de disponibilidade por região e horário
- Agente de IA para sugestão de rota otimizada do dia baseada em disponibilidade predita
- Integração com Google Calendar para sincronizar agenda de visitas
- Módulo de notas privadas por médico (perfil, preferências, histórico de relacionamento)
- API aberta para laboratórios integrarem dados do MedWaze em seus próprios CRMs
- Verificação de reportes por consenso: status só muda com 2+ reportes consistentes
- Histórico de visitas com registro fotográfico (foto do consultório para confirmar endereço)

## Riscos Identificados

- Risco de adoção (CRÍTICO): Efeito de rede — a plataforma só tem valor com muitos usuários contribuindo. Mitigação: lançar com um laboratório parceiro comprometido com 20+ propagandistas e implementar gamificação agressiva nas primeiras semanas para criar hábito de reporte.
- Risco de qualidade dos dados: Reportes falsos ou farming de XP podem destruir a confiabilidade. Mitigação: AgenteDetectorAnomalias + sistema de reputação por usuário + moderação por gestores distritais.
- Risco legal/LGPD: Dados de localização de médicos e padrões de comportamento são dados sensíveis. Mitigação: consultar advogado especializado em LGPD antes do lançamento, anonimizar dados nos logs, implementar consentimento explícito no cadastro e política de privacidade clara.
- Risco técnico de WebSocket em escala: Múltiplas conexões simultâneas com conectividade móvel instável pode causar estados inconsistentes. Mitigação: implementar reconexão automática, updates otimistas no cliente e fallback para polling HTTP quando WebSocket falhar.
- Risco de precisão da IA: Predições incorretas do AgentePredicaoDisponibilidade podem gerar desconfiança. Mitigação: exibir sempre o percentual de confiança da predição, mostrar baseado em N reportes, e permitir que o usuário ignore/reporte a predição como incorreta.
- Risco de resistência de médicos: Médicos podem se sentir monitorados sem consentimento. Mitigação: posicionar o produto exclusivamente para o lado do propagandista, não compartilhar dados com pacientes, e considerar opt-out para médicos que solicitarem.

## Resumo das Referências Analisadas

A análise do site waze.com/pt-BR revelou 4 princípios fundamentais incorporados no MedWaze: (1) INTELIGÊNCIA COLETIVA — 'Com tantas pessoas contribuindo, parece que faço parte de algo maior' — esse senso de comunidade foi incorporado na gamificação com XP e ranking, transformando cada reporte individual em contribuição para toda a rede de propagandistas; (2) TEMPO REAL E RECÁLCULO CONTÍNUO — 'O Waze sabe quando uma rota está desatualizada' — o sistema de TTL de 4 horas no Redis e WebSocket garante que status obsoletos são substituídos por informações frescas, assim como o Waze recalcula rotas; (3) ALERTAS PROATIVOS — 'Receba um alerta quando for a hora de sair' — implementado no AgenteBriefingDiario que notifica propagandistas às 07:00 com o roteiro otimizado do dia antes mesmo de saírem de casa; (4) CORREÇÃO COLABORATIVA DE DADOS — 'Encontrei pontos incorretos no mapa. Minha correção podia ser vista no dia seguinte' — implementado na opção de reporte 'Endereço Incorreto / Mudou' com a maior pontuação XP (+30) para incentivar a manutenção da qualidade dos dados cadastrais de médicos.
