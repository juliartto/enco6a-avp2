# 📚 Agenda Virtual Escolar

> Sistema de notificações para responsáveis acompanharem anotações e atividades escolares enviadas pelos professores, evitando que mensagens importantes registradas na agenda física da criança passem despercebidas.

**Domínio:** Educação  
**Disciplina:** Engenharia de Software — 2026/1  

---

## Parte 1 — Engenharia de Requisitos

---

### 🧩 Tarefa 1.1 — Proposta de Tema

> Descreva em até 10 linhas o problema, os usuários e a relevância.
_[O sistema é um aplicativo, simulando uma agenda, que manda notificações para os responsáveis cadastrados quando há anotações novas e lembretes de datas de eventos ou reuniões.
  É voltado para os responsáveis e professores de alunos principalmente no Ensino Fundamental I ou Pré-escola.
  Visa evitar que o aluno perca o aviso, esconda a agenda o que o responsável simplesmente esqueça de fazer a leitura diária da agenda.]_

---

### 🎤 Tarefa 1.2 — Planejamento de Entrevista

**Objetivo da entrevista**
_[A entrevista deve ser realizada com um responsável de um aluno, visando saber porque notificações seriam mais efetivas e se uma agenda virtual é mais prática no cotidiano que uma agenda física.]_

#### 🔎 Perguntas abertas sobre o problema (mínimo 3)

1. _[Você já se esqueceu de um evento escolar ou deixou de ajudar com uma atividade por não saber dela?]_
2. _[Se você pudesse mudar uma única coisa na forma como a escola se comunica com você hoje, o que seria?]_
3. _[O que mais não se encaixa na sua rotina com o atual meio de comunicação da escola?]_
4. _[No cotidiano, quando você tem acesso à agenda escolar física do tutelado?]_
5. _[Quem mais cuida da agenda do tutelado?]_
6. _[Você enfrenta alguma dificuldade utilizando outros aplicativos de agenda para anotar as atividades do tutelado?]_
7. _[Como uma agenda virtual somente para avisos escolares ajudaria a evitar esquecimentos?]_
8. _[Tem algum aspecto da rotina escolar do seu filho que você acha importante eu entender mas que não apareceu nas minhas perguntas?]_

**Minha reflexão:**
_[As perguntas feitas têm como objetivo estabelecer como a agenda deve funcionar para conforto dos responsáveis. 
  Conhecer mais sobre a rotina é ideal para saber se os responsáveis vão aderir a agenda virtual, se conseguem olhar as notificações em outros momentos do dia quando estão longe da agenda física,
  além de sabermos se existe algum problema não contemplado apenas pelas perguntas já feitas e que os responsáveis consideram importante considerar.]_

---

### 👤 Tarefa 1.3 — Histórias de Usuário

> Exatamente 5 histórias no formato:
> _Como [perfil], quero [ação] para [benefício]._

---

#### História 1

_[Como responsável por um aluno, quero receber notificações push no meu celular sempre que o professor adicionar um novo recado ou tarefa, 
  para que eu não perca comunicados importantes mesmo na correria do dia a dia longe da agenda física.]_.

**Critérios de aceitação:**
- [ ] _[O sistema deve enviar uma notificação push para o dispositivo do responsável no exato momento em que o professor publicar o aviso.]_
- [ ] _[Ao clicar na notificação, o aplicativo deve abrir diretamente na tela do respectivo recado.]_
- [ ] _[O usuário deve conseguir silenciar temporariamente as notificações durante o horário de trabalho nas configurações do aplicativo.]_

**Prioridade:** _Alta_  
**Justificativa:** _[A notificação ativa é o núcleo da sua proposta de sistema. Ela ataca diretamente o problema de recados passarem despercebidos.]_

---

#### História 2

_[Como professor, quero poder enviar o mesmo recado para a turma inteira simultaneamente, para otimizar meu tempo de trabalho e evitar a escrita manual em dezenas de agendas físicas.]_.

**Critérios de aceitação:**
- [ ] _[A interface de criação de recado deve ter opções para selecionar "Turma Inteira" ou selecionar "Alunos Específicos".]_
- [ ] _[O sistema deve permitir anexar um arquivo de imagem (ex: foto do quadro com a tarefa) à mensagem.]_
- [ ] _[Ao concluir o envio, o sistema deve exibir uma mensagem de confirmação de que os avisos foram disparados.]_

**Prioridade:** _Alta_  
**Justificativa:** _[Para que a agenda virtual funcione para os responsáveis, 
                     o sistema precisa ser extremamente prático para quem insere os dados. Sem essa facilidade, os professores não adotarão a ferramenta.]_

---

#### História 3

_[Como professora, quero visualizar um relatório de quais responsáveis já leram o recado enviado, 
  para ter certeza de que a comunicação foi efetiva ou identificar quem precisa ser contatado de outra forma.]_.

**Critérios de aceitação:**
- [ ] _[Abaixo do recado enviado, o professor deve visualizar uma lista indicando "Visualizado por" e "Pendente".]_
- [ ] _[O sistema deve registrar a data e o horário da primeira visualização de cada usuário.]_
- [ ] _[O evento de visualização deve ser acionado assim que o responsável abrir a tela de detalhes da mensagem.]_

**Prioridade:** _Média_  
**Justificativa:** _[Essa funcionalidade digitaliza o processo de "assinar a agenda" física, sendo essencial para garantir a rastreabilidade e a segurança institucional da escola.]_

---

#### História 4

_[Como responsável por um aluno, quero visualizar um calendário interativo no aplicativo e receber lembretes na véspera de reuniões e eventos, para conseguir organizar minha rotina pessoal com antecedência.]_.

**Critérios de aceitação:**
- [ ] _[O aplicativo deve ter uma aba "Calendário", marcando visualmente os dias com eventos agendados para o aluno.]_
- [ ] _[O sistema deve disparar um lembrete automático (notificação) 24 horas e 2 horas antes de eventos classificados como "Reunião" ou "Avaliação".]_
- [ ] _[Deve haver uma opção para exportar o evento escolar para o calendário nativo do smartphone (Google Agenda/Apple Calendar).]_

**Prioridade:** _Média_  
**Justificativa:** _[Embora seja um diferencial de grande valor apontado nas entrevistas (para evitar esquecimentos), 
                     o sistema inicial já resolve a dor principal apenas com os avisos, podendo o calendário ser integrado num segundo momento do ciclo de vida do software.]_

---

#### História 5

_[Como pai/mãe, quero poder vincular mais de um responsável ao perfil do meu filho, para que outros cuidadores da família (como o outro genitor ou avós) também possam ajudar no acompanhamento escolar.]_.

**Critérios de aceitação:**
- [ ] _[A tela de perfil do aluno deve possuir uma opção "Adicionar Responsável", permitindo convidar outro usuário via e-mail ou código.]_
- [ ] _[As notificações de um novo recado devem ser disparadas para todos os responsáveis atrelados ao aluno simultaneamente.]_
- [ ] _[O sistema deve limitar a quantidade de responsáveis vinculados a no máximo 4 por aluno, por questões de segurança de dados.]_

**Prioridade:** _Baixa_  
**Justificativa:** _[Resolve uma situação comum na dinâmica familiar moderna identificada nas entrevistas ("Quem mais cuida da agenda").
                     Aumenta a adesão, mas as funcionalidades de envio e leitura básica precisam estar operacionais antes dessa implementação.]_

---

**Minha reflexão:**
_[As histórias são extremamanete imporantes para saber quais features são de maior importância para sempre implementados primeiro no sistema e quais tratão mais aderência dos usuários.
  Sem as informações providas pelos entrevistados, não seria possível fazer um sistema que seja confortável e adequado o suficiente para substituir a agenda física já estabelecida na rotina.]_

---

### ✅ Tarefa 1.4 — Validação de Requisitos

> Escolha 2 das 5 histórias acima e aplique verificação de completude e consistência.

#### História escolhida #1: _[História 1]_

**Ambiguidades nos critérios de aceitação**

Ambiguidades: "Exato momento" ignora possíveis lentidões de sistema; "silenciar" não deixa claro se é uma configuração manual ou automática.

Conflitos: O recurso de envio em lote (História 2) pode causar um "spam" de notificações no celular do responsável.

A esclarecer: Avisos urgentes devem ignorar o "modo silencioso"? Ler o recado só pela barra de notificações do celular é o suficiente para o responsável?

---

#### História escolhida #2: _[História 3]_

Ambiguidades: Se o usuário ler a mensagem pela notificação push do celular (sem abrir o app), o sistema registrará um falso "não lido".

Conflitos: Com a função de múltiplos cuidadores (História 5), a regra falha ao não definir o que acontece se apenas um dos pais ler a mensagem.

A esclarecer: Basta um familiar ler para a escola considerar o aviso entregue? A partir de quantos dias "não lido" a escola deve intervir?
---

#### 🔍 Revisão crítica

> Dentre as 5 histórias, qual seria removida se o escopo precisasse ser reduzido pela metade?

**História removida:** _[História 5]_

**Justificativa:** _[Essa história teria seus critérios fora do escopo porque é fornece features adicionais, o problema principal já teria sido resolvido com a agenda virtual para o responsável principal.]_
---
