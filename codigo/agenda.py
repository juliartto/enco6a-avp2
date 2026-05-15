from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass
class Recado:
    """Recado publicado por um professor."""
    id: int
    autor: str
    titulo: str
    conteudo: str
    turma: str
    data: datetime = field(default_factory=datetime.now)

class Observador(ABC):
    """Interface do Observer: define como um inscrito recebe avisos."""

    @abstractmethod
    def receber_notificacao(self, recado: Recado) -> None:
        ...


class Responsavel(Observador):
    """Observer concreto: o responsável recebe push e guarda o recado."""

    def __init__(self, nome: str, aluno: str):
        self.nome = nome
        self.aluno = aluno
        self.recados_recebidos: List[Recado] = []

    def receber_notificacao(self, recado: Recado) -> None:
        self.recados_recebidos.append(recado)
        print(f"  📱 PUSH para {self.nome}: '{recado.titulo}' ({recado.autor})")



class CentralDeNotificacoes:
    _instancia = None  # referência única da classe

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._inscricoes: Dict[str, List[Observador]] = {}
        return cls._instancia

    def inscrever(self, aluno: str, observador: Observador) -> None:
        """Vincula um responsável a um aluno (suporta múltiplos por aluno)."""
        self._inscricoes.setdefault(aluno, []).append(observador)

    def publicar_recado(self, recado: Recado, alunos: List[str]) -> None:
        print(f"\n📝 Recado publicado por {recado.autor}: '{recado.titulo}'")
        for aluno in alunos:
            for obs in self._inscricoes.get(aluno, []):
                obs.receber_notificacao(recado)



def main():
    print("=" * 60)
    print("AGENDA VIRTUAL ESCOLAR — Protótipo")
    print("=" * 60)

    # Verifica o Singleton
    central_a = CentralDeNotificacoes()
    central_b = CentralDeNotificacoes()
    assert central_a is central_b, "Singleton falhou!"
    print(f"\n✓ Singleton: central_a is central_b → {central_a is central_b}")

    # Cadastra responsáveis
    pai_joao  = Responsavel("Carlos (pai)", aluno="João")
    mae_joao  = Responsavel("Ana (mãe)",    aluno="João")
    mae_maria = Responsavel("Beatriz",      aluno="Maria")
    avo_pedro = Responsavel("Dona Cida",    aluno="Pedro")

    central_a.inscrever("João",  pai_joao)
    central_a.inscrever("João",  mae_joao)   # múltiplos responsáveis por aluno
    central_a.inscrever("Maria", mae_maria)
    central_a.inscrever("Pedro", avo_pedro)

    # HU2: professora publica recado para a turma inteira
    recado = Recado(
        id=1,
        autor="Profa. Helena",
        titulo="Lição de casa",
        conteudo="Página 42 do livro de matemática até sexta-feira.",
        turma="3A",
    )
    # HU1: cada responsável recebe um push
    central_a.publicar_recado(recado, alunos=["João", "Maria", "Pedro"])

    # Conferência
    print("\n--- Conferência ---")
    for r in (pai_joao, mae_joao, mae_maria, avo_pedro):
        print(f"  {r.nome}: {len(r.recados_recebidos)} recado(s) recebido(s)")


if __name__ == "__main__":
    main()
