# 📚 Agenda Virtual Escolar — Parte 2

---

## 🏗️ Padrão Arquitetural

**Escolha:** *Cliente-Servidor em camadas, com Pub/Sub para notificações.*

**Justificativa:** o sistema é, em essência, um app móvel que conversa com um servidor central. A estratificação em camadas permite entregar primeiro as histórias de prioridade Alta (HU1 e HU2) e acomodar as demais em evoluções posteriores, sem comprometer a estrutura. Já o Pub/Sub desacopla a publicação do recado do envio efetivo dos pushes aos múltiplos responsáveis vinculados (HU5) — sem ele, o Serviço de Recados precisaria conhecer toda a topologia de inscritos, o que rapidamente se torna um problema de manutenção.

---

## 🗺️ Componentes e Relacionamentos

```
Clientes Móveis
  ├─ App Responsável
  └─ App Professor
        ↓ (HTTPS)
API Gateway
        ↓
Serviços
  ├─ Recados ──── publica evento "NovoRecado" ──→ Notificações
  ├─ Usuários                                          ↓
  ├─ Calendário                                    FCM / APNs
  └─ Notificações                                      ↓
        ↓                                         App Responsável
Domínio (Aluno, Responsável, Professor, Turma,
         Recado, Evento, Visualização)
        ↓
Banco de Dados
```

---

## ⚙️ Responsabilidades

| Componente | Responsabilidade |
|------------|------------------|
| **App Responsável** | Recebe pushes e exibe recados/calendário (HU1, HU4) |
| **App Professor** | Cria recados e consulta relatório de leitura (HU2, HU3) |
| **API Gateway** | Autenticação e roteamento |
| **Serviço de Recados** | Persiste recados e publica o evento `NovoRecado` (HU2) |
| **Serviço de Usuários** | Cadastro e vinculação de múltiplos responsáveis (HU5) |
| **Serviço de Calendário** | Eventos e lembretes (24h / 2h antes — HU4) |
| **Serviço de Notificações** | Dispara pushes via FCM/APNs (HU1) |
| **Domínio** | Entidades do negócio e suas relações |
| **Banco de Dados** | Persistência relacional |

---

## ⚖️ Trade-off

**Latência vs. HU1.** A HU1 exige notificação no "exato momento", mas cada requisição precisa atravessar várias camadas (Gateway → Serviço → Domínio → Persistência → Evento → Notificações → FCM), o que pode atrasar a entrega em horários de pico. **Mitigação:** inserir uma fila de mensagens entre Recados e Notificações, ao custo de mais complexidade operacional.

---

**Minha reflexão:** *Faz sentido começar síncrono para validar logo as histórias. O ponto frágil é depender do FCM/APNs bloqueando a requisição principal, sob carga isso quebra, e já vi o mesmo padrão falhar em integrações com APIs externas. A fila entra cedo ou tarde, com toda a dor de gerenciar workers e cenários de falha que isso traz.*

---

## 💻 Protótipo Funcional

Implementação em Python que atende **HU1** (responsável recebe push quando há novo recado) e **HU2** (professor envia recado para a turma inteira de uma vez).

- **Arquivo:** `agenda.py` — contém modelos, padrões e demonstração.
- **Como rodar:** `python3 agenda.py`

---

## 🧩 Padrões de Projeto Utilizados

### 1. Singleton (criacional)

Garante que exista **uma única instância** da `CentralDeNotificacoes` em todo o sistema — qualquer parte do código que solicite uma central recebe sempre o mesmo objeto, com as mesmas inscrições já registradas.

**Diagrama aplicado ao projeto:**

```
   ┌─────────────────────────────────────┐
   │       CentralDeNotificacoes         │
   ├─────────────────────────────────────┤
   │ - _instancia : CentralDeNotificacoes│  ← guarda a única instância
   │ - _inscricoes : dict                │
   ├─────────────────────────────────────┤
   │ + __new__()       → retorna sempre  │
   │                     a mesma instância│
   │ + inscrever()                       │
   │ + publicar_recado()                 │
   └─────────────────────────────────────┘
              ▲             ▲
              │             │
       central_a       central_b      ← apontam para o MESMO objeto
       (em main.py)    (em main.py)
```

**Onde foi aplicado:** `agenda.py`, método `__new__` da classe `CentralDeNotificacoes`:

```python
class CentralDeNotificacoes:
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inscricoes: Dict[str, List[Observador]] = {}
        return cls._instancia
```

Verificação na função `main()`:

```python
central_a = CentralDeNotificacoes()
central_b = CentralDeNotificacoes()
assert central_a is central_b   # True
```

---

### 2. Observer (comportamental)

Quando um novo recado é publicado (HU2), todos os responsáveis vinculados aos alunos-alvo são notificados automaticamente (HU1), **sem que o publicador precise conhecê-los nominalmente**. Esse desacoplamento é precisamente o que o padrão Observer entrega.

**Diagrama aplicado ao projeto:**

```
   ┌─────────────────────────┐                ┌──────────────────┐
   │   CentralDeNotificacoes │  ── notifica ─►│    Observador    │ (ABC)
   │        (Subject)        │     todos os   ├──────────────────┤
   ├─────────────────────────┤    inscritos   │ + receber_       │
   │ + inscrever(aluno, obs) │                │   notificacao()  │
   │ + publicar_recado(...)  │                └─────────▲────────┘
   └─────────────────────────┘                          │
                                                        │ implementa
                                                        │
                                              ┌─────────┴──────────┐
                                              │    Responsavel     │
                                              ├────────────────────┤
                                              │ - nome             │
                                              │ - aluno            │
                                              │ - recados_recebidos│
                                              ├────────────────────┤
                                              │ + receber_         │
                                              │   notificacao()    │
                                              └────────────────────┘
```

**Onde foi aplicado:** `agenda.py`, interface `Observador`, classe concreta `Responsavel` e método `publicar_recado` da `CentralDeNotificacoes`:

```python
class Observador(ABC):
    @abstractmethod
    def receber_notificacao(self, recado: Recado) -> None: ...

class Responsavel(Observador):
    def receber_notificacao(self, recado: Recado) -> None:
        self.recados_recebidos.append(recado)
        print(f"  📱 PUSH para {self.nome}: '{recado.titulo}'")

# O Subject percorre os observadores e dispara o método
def publicar_recado(self, recado, alunos):
    for aluno in alunos:
        for obs in self._inscricoes.get(aluno, []):
            obs.receber_notificacao(recado)
```

---

**Reflexão crítica:** *Observer + Singleton funciona aqui porque tudo fica no mesmo processo. Em produção, com a API rodando em vários workers, o Singleton já não cabe, a instância não é compartilhada entre processos. Quando chegar a esse ponto, a central precisa sair do código e ir para um broker ou Redis.*

---

## 🧪 Testes Automatizados

- **Arquivo:** `test_agenda.py` — usa `unittest`.
- **Como rodar:** `python3 -m unittest test_agenda -v`

Cobrem os dois métodos centrais com três casos cada (sucesso, borda, falha/exceção):

| Método | Sucesso | Borda | Falha/Exceção |
|--------|---------|-------|---------------|
| `inscrever()` | responsável fica na lista do aluno | 4 responsáveis no mesmo aluno (limite da HU5) | instanciar `Observador` (ABC) → `TypeError` |
| `publicar_recado()` | todos os responsáveis recebem o recado | publicar para aluno sem ninguém inscrito não falha | recado `None` → `AttributeError` |

### Estratégia de teste adotada

Foi adotado **teste unitário com isolamento por reset do Singleton**: cada caso roda em um `setUp` que zera `CentralDeNotificacoes._instancia`, evitando que o estado compartilhado entre instâncias contamine os testes seguintes. A escolha por testes unitários é adequada porque o protótipo concentra a lógica em dois métodos puros (sem chamadas externas reais), o que permite verificar comportamento por **asserções diretas no estado dos observadores** (lista `recados_recebidos`) e no dicionário interno de inscrições — sem necessidade de mocks ou infraestrutura adicional.

**Não foram cobertos:**

- a camada de apresentação (clientes móveis) e o API Gateway, pois não existem no protótipo;
- o disparo real para FCM/APNs, pois exigiria integração com serviços externos e mocks de rede;
- cenários de concorrência (vários professores publicando simultaneamente), pois o código atual é síncrono e *single-thread*, e modelá-los exigiria reescrita do `publicar_recado` com locks ou filas.

---

**Reflexão crítica:** *O mais difícil de testar foi o `__new__` do Singleton. Como `_instancia` e `_inscricoes` persistem entre casos, cada teste precisa zerar esse estado manualmente no `setUp`. Em projeto maior isso vira teste flaky, a falha de um caso passa a depender da ordem em que outro rodou antes. A correção honesta seria injeção de dependência, mas a essa altura o padrão já contaminou todo código que consome a central.*

---
