# Documento de Requisitos — MedWaze

> **Versão:** 1.3 · **Data:** 07/07/2026  
> Este documento descreve o que o MedWaze faz, para quem, e como — em linguagem acessível para toda a equipe, incluindo não-técnicos.

---

## 1. O que é o MedWaze (em uma frase)

MedWaze é uma plataforma colaborativa que responde, em tempo real, a pergunta que nenhum sistema do mercado responde hoje: **"Em qual endereço esse médico está, em quais dias da semana, e ele está lá agora?"**

### O que MedWaze NÃO é
É importante deixar claro o que o MedWaze **não** é, para não confundir com sistemas já existentes:

| Sistema | O que faz | MedWaze substitui? |
|---|---|---|
| Viva Real | Base de dados de médicos e endereços comprada por laboratórios | ❌ Não — MedWaze complementa com verificação em campo |
| SalesPharma / Salesforce Health | Lançamento de visitas, CRM, cobertura de médicos | ❌ Não — MedWaze não é sistema de visita |
| Google / Internet | Endereços públicos desatualizados | ❌ Não — MedWaze é a camada verificada por quem foi até lá |

**MedWaze é a camada de inteligência em tempo real que os outros sistemas não têm.** O Viva tem endereço, mas não sabe se o médico atende ali às terças ou às quintas. O MedWaze sabe — porque alguém da rede foi até lá e confirmou.

---

## 2. O problema real (contexto do mercado)

Os laboratórios farmacêuticos têm uma ferramenta chamada **Audit** que identifica *onde* as receitas de um médico estão sendo dispensadas (em qual farmácia/cidade). Isso revela onde o médico está **de fato** atendendo — mas não diz *em qual clínica*, *em quais dias* e *se ele está lá agora*.

**O gap que existe hoje:**

> O Audit mostra que o Dr. X está prescrevendo em Betim.  
> A internet mostra endereço em BH.  
> O Viva talvez tenha um endereço de Betim cadastrado.  
> Mas nenhum deles responde: *quais dias da semana ele atende em Betim? De que horas a que horas? Ele está lá hoje?*  
> O rep descobre isso só quando vai até lá — e às vezes perde o dia.

**Como o mercado funciona hoje (contexto importante):**
- Laboratórios compram bases de dados de médicos (ex: Viva Real, SalesPharma) — essas bases são **compartilhadas entre todos os laboratórios** que assinam o mesmo serviço
- Quando um laboratório atualiza um endereço no Viva, todos os outros labs que usam o Viva veem a atualização
- Isso é intencional: quanto mais labs atualizando, melhor o dado para todos — não é sobre exclusividade, é sobre **penetração** (chegar até o médico)
- A classificação de médicos por volume de prescrição (cat 1 a 5 por molécula) é compartilhada — quando um médico vira cat 1, todos os labs vão atrás dele
- **MedWaze segue o mesmo modelo:** rede aberta, todos os reps de todos os labs contribuem e se beneficiam

**Por que os endereços são sempre errados:**
- 80–90% dos médicos metropolitanos atendem em múltiplas cidades (ex: 2 dias em Betim, 3 em BH)
- Médicos têm **alta rotatividade de consultório** — não são empreendedores, trabalham para clínicas de terceiros e trocam com frequência por demissão ou redução de jornada
- Nenhum sistema captura os *dias da semana por endereço* — apenas o endereço em si
- Médicos não atualizam seus próprios cadastros nas plataformas

**O MedWaze resolve isso** com inteligência coletiva dos reps em campo — a mesma lógica do Viva (rede compartilhada), mas com o dado que o Viva não tem: **verificação em campo + dias da semana + status ao vivo**.

---

## 3. Quem usa o MedWaze?

| Papel | Quem é | O que faz no MedWaze | Incentivo |
|---|---|---|---|
| **Representante / Propagandista** | Profissional de vendas de laboratório | Reporta status, corrige endereços, descobre novos locais de atendimento | XP, ranking, visitas mais produtivas |
| **Secretária do consultório** | Responsável pela agenda do médico | Confirma ou edita a agenda oficial do médico (dias, horários, endereço) | Garante que as amostras do laboratório cheguem no horário certo |
| **Gestor Distrital** | Líder da equipe de campo | (v2) Monitora produtividade do time via dashboard | Visão gerencial em tempo real |
| **Médico** | Clínico, especialista, etc. | (v2) Pode confirmar sua própria agenda | Recebe amostras na hora certa, evita visitas fora de hora |

### A secretária como fonte de dados privilegiada
A secretária tem o dado mais confiável sobre a agenda do médico — ela gerencia essa agenda diariamente. O incentivo para ela participar é direto: **as amostras do laboratório chegam para o médico certo, no local certo, no dia certo**. Sem o dado atualizado, o rep pode ir ao consultório errado e perder a oportunidade de entrega.

No MVP, a secretária pode ser cadastrada com um perfil especial que permite editar a agenda do médico diretamente, sem precisar do fluxo de reporte de status.

---

## 4. Quem são os usuários (personas)

### 4.1 João — Propagandista de Campo
- Trabalha para um laboratório farmacêutico
- Visita de 8 a 12 médicos por dia em múltiplas cidades
- Usa smartphone Android em campo, muitas vezes com internet instável
- **Problema 1:** chega no consultório e o médico não está lá — perde 30–60 min por visita improdutiva
- **Problema 2:** o Audit mostra que o Dr. X está prescrevendo em Betim, mas o sistema só tem endereço de BH — ele não sabe onde encontrar o médico em Betim
- O que ele precisa: saber **onde** e **quando** o médico atende, e se **está lá agora**

### 4.2 Carla — Representante com Carteira Multi-Cidade
- Carteira de 40+ médicos em 3 cidades diferentes
- Planeja a rota de visitas na noite anterior cruzando dados do Audit com agenda pessoal
- **Problema:** o endereço no CRM está errado para 30–40% dos médicos que atendem em múltiplos locais
- O que ela precisa: uma base colaborativa de endereços verificados por quem foi até lá

---

## 5. Fluxo principal — O que o usuário faz no app

### 4.1 Consultando o status antes de sair
1. João abre o MedWaze às 7h da manhã
2. Vê a lista dos médicos da sua região com badges coloridas:
   - 🟢 **Verde** = está recebendo normalmente
   - 🟡 **Amarelo** = está atrasado (mas vai atender)
   - 🔴 **Vermelho** = não está atendendo hoje
3. Filtra por "Com Alertas" para ver só os médicos problemáticos
4. Decide pular a visita ao Dr. Roberto (vermelho, reportado 1h atrás) e priorizar a Dra. Mariana (verde)
5. Segue para o consultório com mais confiança

### 4.2 Reportando o status ao chegar no consultório
1. João chega no consultório do Dr. Carlos
2. Abre o card do Dr. Carlos no app
3. Clica em **"Reportar"**
4. Escolhe uma das 4 opções:
   - ✅ Está recebendo (+10 XP)
   - ⏰ Está atrasado (+15 XP)
   - ❌ Não está atendendo (+20 XP)
   - 📍 Endereço incorreto / mudou (+30 XP)
5. Confirma — o status do Dr. Carlos atualiza **instantaneamente** para todos os outros representantes que estão vendo o mesmo médico
6. João recebe uma notificação "+15 XP" na tela

### 5.3 Acompanhando o feed da comunidade
1. Carla abre o app e vê o feed "ao vivo":
   - "Rafael reportou Dr. Carlos como **Atrasado** · 5 min atrás"
   - "Lucas reportou Dra. Mariana como **Recebendo** · 3 min atrás"
2. Ela conclui que vale a pena ir visitar a Dra. Mariana agora

### 5.4 Corrigindo o endereço de um médico (fluxo do Audit)
1. O Audit mostra que o Dr. X está prescrevendo em Betim
2. João vai a Betim e encontra o Dr. X na Clínica Santa Cruz, às terças e quintas
3. No app, João abre o card do Dr. X e reporta **"Endereço incorreto"**
4. Um formulário aparece pedindo: novo endereço, dias da semana, horário
5. João preenche e confirma — ganha +30 XP
6. O card do Dr. X agora mostra dois locais de atendimento:
   - BH: Av. Afonso Pena · Seg, Qua, Sex
   - Betim: Clínica Santa Cruz · Ter, Qui *(verificado por João, hoje)*
7. Todos os reps que acompanham o Dr. X veem a atualização imediatamente

---

## 6. Requisitos Funcionais (o que o sistema DEVE fazer)

### 6.1 Cadastro e Localização de Médicos
- **80–90% dos médicos metropolitanos atendem em múltiplos locais** — múltiplos endereços por médico é a regra, não a exceção
- Cada médico tem N locais de atendimento. Cada local registra: endereço, **dias da semana**, horário, e data da última verificação em campo
- Os **dias da semana por endereço** são o dado mais valioso — é o que nenhuma outra plataforma tem
- Médicos têm **alta rotatividade de consultório** (trocam de clínica com frequência) — endereços envelhecem rápido
- No MVP, médicos são importados via **planilha Excel** — base comprada de fornecedor (ex: Viva, SalesPharma) ou fornecida pelo cliente
- O Audit do laboratório (exportado em Excel) é cruzado com o cadastro: médicos com receitas em cidades sem endereço cadastrado naquela cidade aparecem com alerta **"Localização a investigar em [cidade]"**
- O status em tempo real ("está recebendo agora") é vinculado ao **local de atendimento do dia**, não ao médico em geral
- Locais confirmados por 2+ reps independentes recebem selo **"Verificado em campo"**
- Locais sem verificação há mais de 60 dias são marcados como **"Verificação pendente"**

### 6.2 Visualização de Status
- O usuário vê todos os médicos em lista com badge colorida de status
- Badge verde pulsa suavemente (indica ativo/dinâmico)
- Cada card exibe: quem fez o último reporte, há quanto tempo, e total de reportes do médico
- Status desatualizado há mais de 4 horas retorna automaticamente para "sem informação"

### 6.3 Reporte de Status
- O usuário pode reportar o status de qualquer médico da lista
- Ao confirmar o reporte, o status atualiza em tempo real para todos os usuários conectados
- O mesmo usuário não pode reportar o mesmo médico mais de uma vez em 2 horas (proteção contra spam)
- Cada reporte registra: quem reportou, quando, qual status, e em qual local de atendimento
- **Nova opção de reporte:** "Médico não trabalha mais aqui" (+25 XP) — para capturar a alta rotatividade de consultórios; esse reporte inicia um fluxo de revisão do endereço

### 6.4 Correção e Enriquecimento de Endereços
- Ao reportar "Endereço incorreto", o usuário pode:
  - Corrigir o endereço existente
  - Adicionar um novo local de atendimento (para médicos multi-cidade)
  - Informar os dias da semana e horário daquele local
- Cada correção de endereço aceita pela comunidade vale **+30 XP** (maior pontuação do sistema)
- Endereços corrigidos ficam marcados como "verificado em campo por [rep] em [data]"
- Se dois ou mais reps confirmam o mesmo endereço independentemente, ele ganha selo de **"Confirmado"**

### 6.5 Importação do Audit (Excel)
- O sistema aceita upload de planilha Excel com dados do Audit do laboratório
- Campos esperados: CRM do médico, cidade onde a receita caiu, volume de receitas, período
- O sistema cruza com o cadastro de médicos: se um médico tem receitas em uma cidade sem endereço cadastrado naquela cidade, ele aparece com alerta **"Localização a investigar em [cidade]"**
- Isso direciona os reps para as investigações de campo de maior impacto comercial

### 6.6 Gamificação
- Cada reporte concede XP ao usuário conforme tabela:
  | Tipo de Reporte | XP | Motivo do valor |
  |---|---|---|
  | Está recebendo | +10 XP | Confirmação de disponibilidade |
  | Está atrasado | +15 XP | Evita espera desnecessária de outros reps |
  | Não está atendendo | +20 XP | Evita deslocamento improdutivo |
  | Médico não trabalha mais aqui | +25 XP | Inicia revisão de endereço — dado crítico |
  | Endereço/local confirmado em campo | +30 XP | Contribuição máxima — constrói a base |
- O XP total do usuário é exibido no cabeçalho do app em tempo real
- Secretárias que confirmam agenda oficial ganham bônus de XP (valor a definir com Felipe)

### 6.7 Filtros e Busca
- Filtros rápidos: **Todos** / **Disponíveis** / **Com Alertas**
- Barra de pesquisa por nome do médico ou especialidade (resultado aparece enquanto digita)
- Os contadores dos filtros se atualizam automaticamente quando status muda

### 6.8 Feed da Comunidade
- Seção "ao vivo" exibindo os últimos reportes de todos os usuários
- Cada item mostra: quem reportou, qual médico, qual status, há quanto tempo, e XP ganho
- Feed atualiza automaticamente sem recarregar a página

### 6.9 Autenticação (MVP simplificado)
- No protótipo: usuário digita um apelido na primeira visita (salvo localmente no dispositivo)
- No produto final: login via Magic Link por e-mail (sem senha) ou Google

---

## 7. Requisitos Não-Funcionais (como o sistema deve se comportar)

| Requisito | Meta |
|---|---|
| **Mobile-first** | Interface desenhada para smartphone (tela pequena, uso com uma mão) |
| **Tempo de atualização** | Status de um reporte deve aparecer para outros usuários em menos de 2 segundos |
| **Offline parcial** | Lista de médicos deve ser consultável sem internet (cache local) |
| **Performance mobile** | Lighthouse score > 90 em dispositivo Android intermediário |
| **Conectividade instável** | Reconectar automaticamente ao WebSocket se a conexão cair em campo |

---

## 8. O que NÃO faz no MVP (fora do escopo)

| Feature | Por quê não está no MVP |
|---|---|
| Mapa interativo com pins dos médicos | Complexidade alta, não é o cerne da proposta de valor |
| App nativo iOS / Android | PWA (site instalável no celular) é suficiente para o MVP |
| Integração com CRMs farmacêuticos | Dados de médicos vêm de planilha fornecida pelo cliente |
| Notificações push nativas | Implementado na Fase 3, após validação do MVP |
| Cadastro de médicos por interface | Admin insere diretamente no banco via seed |
| Agentes de IA (predição, briefing) | Fase 3 — dependem de histórico acumulado de reportes |
| Dashboard gerencial | Fase 3 — aguarda feedback dos gestores distritais |
| Verificação de reportes por consenso | Complexidade desnecessária no MVP |
| Histórico fotográfico de consultórios | Feature de v2 |

---

## 9. Critérios de Aceite do MVP

O MVP está pronto quando **todos** os itens abaixo funcionam corretamente:

- [ ] Um representante consegue ver a lista de médicos com status atualizado sem precisar recarregar a página
- [ ] Ao reportar um status, outro usuário (em outro dispositivo/browser) vê a mudança em menos de 3 segundos
- [ ] O XP do usuário aumenta após cada reporte e persiste ao fechar e reabrir o app
- [ ] Os filtros "Disponíveis" e "Com Alertas" mostram apenas os médicos corretos
- [ ] A busca por nome ou especialidade retorna resultados corretos
- [ ] O mesmo usuário não consegue reportar o mesmo médico duas vezes em menos de 2 horas
- [ ] A interface é utilizável em smartphone sem zoom ou scroll horizontal
- [ ] O app funciona com conexão 3G instável (reconecta automaticamente se cair)

---

## 10. Perguntas Respondidas

| Questão | Resposta |
|---|---|
| O Audit pode exportar dados? | ✅ Sim — enviado via Excel, pode ser importado diretamente |
| Viável engajar secretárias? | ✅ Sim — incentivo é garantia de entrega de amostras no local/dia certo |
| Qual % dos médicos são multi-cidade? | ✅ 80–90% na região metropolitana — é a regra |
| Rede aberta ou separada por laboratório? | ✅ **Rede aberta** — mesmo modelo do Viva; todos os labs compartilham e se beneficiam |
| Concorrentes podem ver dados uns dos outros? | ✅ Sim — a lógica é: mais reps atualizando = dado melhor para todos |
| MedWaze substitui o Viva ou o Salesforce? | ✅ **Não** — é complementar; eles têm o endereço, MedWaze tem os dias da semana + status ao vivo |
| Gestor distrital entra no MVP? | ✅ **Não** — MedWaze não é sistema de lançamento de visitas; gestor já usa Viva/Salesforce para isso |

## 11. Pendências

| Questão | Responsável | Quando |
|---|---|---|
| Qual fornecedor de base de médicos será usado? (Viva, SalesPharma, outro?) | Felipe / Cliente | Antes da Fase 1 |
| Qual o XP/incentivo para a secretária confirmar a agenda? | Felipe | Antes do lançamento beta |
