"""module contains unittest for correlatiom matrix"""

import unittest
from unittest import mock

from types import SimpleNamespace
from gn3.computations.correlation_matrix import fetch_sample_datas
from gn3.computations.correlation_matrix import compute_row_matrix


class TestCorrelationMatrix(unittest.TestCase):
    """test for correlation matrix functions"""

    def test_fetch_sample_datas(self):
        """function to fetch both trait_vals and target_vals"""

        # target_sample and also this_sample

        # target_samples_keys ==target_samples ??????????????

        target_samples = ["C57BL/6J", "DBA/2J", "B6D2F1",
                          "D2B6F1", "BXD1", "BXD2", "BXD5", "BXD6"]

        target_samples_data = {"C57BL/6J": SimpleNamespace(value=1.2),
                               "B6D2F1": SimpleNamespace(value=2.1),
                               "BXD": SimpleNamespace(value=1.1),
                               "BXD12": SimpleNamespace(value=2.2),
                               "BXD5": SimpleNamespace(value=1.2),
                               "BXD6": SimpleNamespace(value=1.1)}

        this_samples_data = {"DBA/2J": SimpleNamespace(value=1.22),
                             "B6D2F1": SimpleNamespace(value=2.3),
                             "BXD1":    SimpleNamespace(value=1.1),
                             "BXD2": SimpleNamespace(value=2.2),
                             "BXD5": SimpleNamespace(value=1.2),
                             "BXD6": SimpleNamespace(value=1.1)}

        expected_target_trait_vals = [2.1, 1.2, 1.1]

        expected_this_trait_vals = [2.3, 1.2, 1.1]

        results = fetch_sample_datas(
            target_samples, target_samples_data, this_samples_data)

        self.assertEqual(results, (expected_this_trait_vals,
                                   expected_target_trait_vals))

    @mock.patch("gn3.computations.correlation_matrix.compute_corr_coeff_p_value")
    @mock.patch("gn3.computations.correlation_matrix.normalize_values")
    def test_compute_row_matrix(self, mock_normalize_vals, mock_corr_computation):
        """Lower left cells list Pearson product-moment correlations;
        upper right cells list Spearman rank order correlations"""

        mock_normalize_vals.side_effect = [
            ([1, 2, 3], [4, 5, 6], 3), ([4.1, 3.2, 1.3], [4.7, 0, 1.2], 3)]
        mock_corr_computation.side_effect = [(0.99, 0.5), (0.510, 3)]
        sample_datas = [("123_at", [[1, 2, 3], [4, 5, 6]]),
                        ("124_at", [[4.1, 3.2, 1.3], [4.7, 0, 1.2]])]
        results = compute_row_matrix(sample_datas)

        corr_row = [["123_at", 0.99, 3], ["124_at", 0.51, 3]]
        pca_row = [0.99, 0.51]

        self.assertEqual(results, [corr_row, pca_row])