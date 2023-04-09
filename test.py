import unittest
from unittest.mock import MagicMock

from pandas.testing import assert_frame_equal
from plotly.graph_objs import Figure

import index  # assuming the original code is in a file named index.py

class Testindex(unittest.TestCase):
    def setUp(self):
        self.df = MagicMock()
        self.df_main = MagicMock(return_value=self.df)
        index.get_data = self.df_main

    def test_get_data(self):
        index.get_data()
        self.df_main.assert_called_once()

    # def test_indexlication(self):
    #     index.indexlication()
    #     self.df_main.assert_called_once()
    #     self.assertIsInstance(index.fig1, Figure)
    #     self.assertIsInstance(index.fig2, Figure)
    #     self.assertIsInstance(index.index.layout, dict)

    # def test_rename_columns(self):
    #     input_df = MagicMock(columns={
    #         'dt_inicio_ativ': 'Data De Início da Atividade',
    #         'dt_sit_cadastral': 'Data Da Ult. Situação Cadastral',
    #         'CNPJs': 'CNPJs',
    #         'capital_social': 'Capital Total',
    #         'med_capital_social': 'Média do Capital Registrado',
    #         'sit_cadastral': 'Situação Cadastral',
    #         'month': 'Mês',
    #         'year': 'Ano',
    #         'UF': 'Estado',
    #         'natureza_juridica': 'Natureza Juridica',
    #     })
    #     expected_output_df = MagicMock(columns={
    #         'Data De Início da Atividade': 'Data De Início da Atividade',
    #         'Data Da Ult. Situação Cadastral': 'Data Da Ult. Situação Cadastral',
    #         'CNPJs': 'CNPJs',
    #         'Capital Total': 'Capital Total',
    #         'Média do Capital Registrado': 'Média do Capital Registrado',
    #         'Situação Cadastral': 'Situação Cadastral',
    #         'Mês': 'Mês',
    #         'Ano': 'Ano',
    #         'Estado': 'Estado',
    #         'Natureza Juridica': 'Natureza Juridica',
    #     })
    #     output_df = index.rename_columns(input_df)
        # assert_frame_equal(output_df, expected_output_df)

if __name__ == '__main__':
    unittest.main()
