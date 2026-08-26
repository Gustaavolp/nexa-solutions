from rest_framework import status
from rest_framework.test import APITestCase

from .models import Chamado


class CriacaoChamadoTests(APITestCase):
    def test_criacao_valida(self):
        resposta = self.client.post(
            "/api/chamados/",
            {"titulo": "Impressora não liga", "descricao": "Sem energia"},
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Chamado.objects.count(), 1)
        self.assertEqual(Chamado.objects.get().titulo, "Impressora não liga")

    def test_criacao_sem_titulo(self):
        resposta = self.client.post(
            "/api/chamados/",
            {"descricao": "Sem energia"},
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.data)
        self.assertEqual(Chamado.objects.count(), 0)


class FiltroStatusTests(APITestCase):
    def setUp(self):
        Chamado.objects.create(titulo="Chamado aberto", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado em andamento", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(
            titulo="Chamado concluído", status=Chamado.Status.CONCLUIDO
        )

    def test_filtro_por_status_valido(self):
        resposta = self.client.get("/api/chamados/?status=ABERTO")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 1)
        self.assertEqual(resposta.data[0]["status"], Chamado.Status.ABERTO)

    def test_filtro_por_status_invalido(self):
        resposta = self.client.get("/api/chamados/?status=INEXISTENTE")

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)

    def test_listagem_sem_filtro_retorna_todos(self):
        resposta = self.client.get("/api/chamados/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta.data), 3)


class IndicadoresTests(APITestCase):
    def setUp(self):
        Chamado.objects.create(titulo="Chamado 1", status=Chamado.Status.ABERTO)
        Chamado.objects.create(titulo="Chamado 2", status=Chamado.Status.ABERTO)
        Chamado.objects.create(
            titulo="Chamado 3", status=Chamado.Status.EM_ANDAMENTO
        )
        Chamado.objects.create(titulo="Chamado 4", status=Chamado.Status.CONCLUIDO)

    def test_indicadores(self):
        resposta = self.client.get("/api/indicadores/")

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.assertEqual(
            resposta.data,
            {
                "total": 4,
                "abertos": 2,
                "em_andamento": 1,
                "concluidos": 1,
            },
        )
