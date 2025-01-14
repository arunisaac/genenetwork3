"""test for biweight script"""
from unittest import TestCase
from unittest import mock

from gn3.computations.biweight import calculate_biweight_corr


class TestBiweight(TestCase):
    """test class for biweight"""

    @mock.patch("gn3.computations.biweight.subprocess.check_output")
    def test_calculate_biweight_corr(self, mock_check_output):
        """test for calculate_biweight_corr func"""
        mock_check_output.return_value = "0.1 0.5"
        results = calculate_biweight_corr(command="Rscript",
                                          path_to_script="./r_script.R",
                                          trait_vals=[
                                              1.2, 1.1, 1.9],
                                          target_vals=[1.9, 0.4, 1.1])

        self.assertEqual(results, (0.1, 0.5))
