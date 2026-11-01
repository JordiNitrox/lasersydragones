#!/usr/bin/env python3
"""
Pruebas unitarias para validar las reglas de sustitución fonética
y detección contextual en limpiar_transcripcion.py
"""

import unittest
from limpiar_transcripcion import aplicar_correcciones_y_auditar

class TestLimpiezaTranscripcion(unittest.TestCase):

    def test_reemplazos_nivel_1_seguros(self):
        casos = [
            ("Llegamos a la piedra del triunfo en el carguero", "Llegamos a la Roca del Drift en el carguero"),
            ("El motor del triunfo se sobrecalentó", "El motor del Drift se sobrecalentó"),
            ("Axel 42 desenfundó su pistola de agujas", "A.Xel 42 desenfundó su pistola de agujas"),
            ("Hablamos con Ring Rey en el taller", "Hablamos con Rim Rey en el taller"),
            ("Ferani Krane dio la orden de disparar", "Ferani Nadaz dio la orden de disparar"),
            ("Subieron a bordo de la Sunrise Maiden", "Subieron a bordo de la Estrella Errante"),
            ("Chischis envió las coordenadas por telepatía", "Chiskisk envió las coordenadas por telepatía"),
            ("El mayordomo Keltusa sirvió las galletitas", "El mayordomo Keltus sirvió las galletitas"),
        ]

        for texto_in, texto_esperado in casos:
            parrafos = [("00:01:00", texto_in)]
            res_parrafos, log_entries, stats = aplicar_correcciones_y_auditar(parrafos)
            texto_out = res_parrafos[0][1]
            self.assertEqual(texto_out, texto_esperado)
            self.assertGreaterEqual(stats["nivel_1"], 1)

    def test_nivel_2_no_falso_positivo_que_elevarse(self):
        # Frase común en español: no debe sustituirse
        frase_ordinaria = "La nave espacial tenía que elevarse sobre las nubes para evitar el radar."
        parrafos = [("00:05:00", frase_ordinaria)]
        res_parrafos, log_entries, stats = aplicar_correcciones_y_auditar(parrafos)
        texto_out = res_parrafos[0][1]

        # No debe haber cambiado a Gevalarsk Nor
        self.assertIn("que elevarse", texto_out)
        self.assertNotIn("Gevalarsk Nor", texto_out)
        self.assertEqual(stats["alertas_dudosas"], 1)
        self.assertEqual(stats["nivel_2_aplicado"], 0)

    def test_nivel_2_reemplazo_con_contexto_valido(self):
        # Frase donde STT oyó 'que elevarse' en presencia del embajador / Eox
        frase_con_contexto = "Fuimos a la embajada de Eox y el embajador que elevarse nos estrechó la mano fría."
        parrafos = [("00:10:00", frase_con_contexto)]
        res_parrafos, log_entries, stats = aplicar_correcciones_y_auditar(parrafos)
        texto_out = res_parrafos[0][1]

        # Debe haberse sustituido porque están las palabras clave 'embajada', 'Eox', 'embajador'
        self.assertNotIn("que elevarse", texto_out)
        self.assertIn("Gevalarsk Nor", texto_out)
        self.assertEqual(stats["nivel_2_aplicado"], 1)
        self.assertEqual(stats["alertas_dudosas"], 0)


if __name__ == "__main__":
    unittest.main()
