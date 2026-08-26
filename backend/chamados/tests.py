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
