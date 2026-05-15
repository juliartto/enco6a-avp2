import unittest

from agenda import CentralDeNotificacoes, Observador, Recado, Responsavel


def _novo_recado() -> Recado:
    return Recado(
        id=1,
        autor="Profa. Helena",
        titulo="Lição de casa",
        conteudo="Página 42 do livro.",
        turma="3A",
    )


class TestInscrever(unittest.TestCase):
    """Testes para CentralDeNotificacoes.inscrever()."""

    def setUp(self):
        # Reseta o Singleton para isolar cada teste
        CentralDeNotificacoes._instancia = None
        self.central = CentralDeNotificacoes()

    def test_sucesso_responsavel_aparece_na_lista(self):
        """Sucesso: responsável vinculado fica nas inscrições do aluno."""
        pai = Responsavel("Carlos", aluno="João")
        self.central.inscrever("João", pai)
        self.assertIn(pai, self.central._inscricoes["João"])

    def test_borda_quatro_responsaveis_no_mesmo_aluno(self):
        """Borda: HU5 prevê até 4 responsáveis por aluno — todos devem caber."""
        responsaveis = [Responsavel(f"R{i}", "João") for i in range(4)]
        for r in responsaveis:
            self.central.inscrever("João", r)
        self.assertEqual(len(self.central._inscricoes["João"]), 4)

    def test_falha_observador_abstrato_nao_instancia(self):
        """Falha/Exceção: Observador é ABC, instanciá-lo deve gerar TypeError."""
        with self.assertRaises(TypeError):
            Observador()  # type: ignore[abstract]


class TestPublicarRecado(unittest.TestCase):
    """Testes para CentralDeNotificacoes.publicar_recado()."""

    def setUp(self):
        CentralDeNotificacoes._instancia = None
        self.central = CentralDeNotificacoes()
        self.recado = _novo_recado()

    def test_sucesso_todos_responsaveis_recebem(self):
        """Sucesso: cada responsável inscrito recebe o recado uma vez."""
        pai = Responsavel("Carlos", "João")
        mae = Responsavel("Ana", "João")
        self.central.inscrever("João", pai)
        self.central.inscrever("João", mae)

        self.central.publicar_recado(self.recado, alunos=["João"])

        self.assertEqual(len(pai.recados_recebidos), 1)
        self.assertEqual(len(mae.recados_recebidos), 1)
        self.assertIs(pai.recados_recebidos[0], self.recado)

    def test_borda_aluno_sem_responsaveis_nao_falha(self):
        """Borda: publicar para aluno sem ninguém inscrito não gera erro."""
        # Não deve lançar exceção
        self.central.publicar_recado(self.recado, alunos=["Fantasma"])
        self.assertNotIn("Fantasma", self.central._inscricoes)

    def test_falha_recado_none_lanca_excecao(self):
        """Falha/Exceção: passar recado None gera AttributeError."""
        pai = Responsavel("Carlos", "João")
        self.central.inscrever("João", pai)
        with self.assertRaises(AttributeError):
            self.central.publicar_recado(None, alunos=["João"])  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main(verbosity=2)
