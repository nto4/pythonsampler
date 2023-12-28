"""
Tests cases for run.read_csv_from_url
Author: https://github.com/nto4
Date: 12/28/2023
"""
import unittest
from unittest.mock import patch, MagicMock
from run import read_csv_from_url

class TestReadCSVFromURL(unittest.TestCase):
    """
    Test cases for read_csv_from_url function.
    """

    def test_successful_fetch(self):
        """
        Test successful fetching of CSV data.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = (
            "date,campaign,clicks\n"
            "2023-01-01,Campaign A,10\n"
            "2023-01-02,Campaign B,15"
        )
        with patch('requests.get', return_value=mock_response):
            result = read_csv_from_url(['date', 'campaign', 'clicks'])
            self.assertTrue('data' in result)
            self.assertEqual(len(result['data']), 2)

    def test_nonexistent_column(self):
        """
        Test handling when a nonexistent column is provided.
        """
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content.decode.return_value = (
            "date,campaign,clicks\n"
            "2023-01-01,Campaign A,10\n"
            "2023-01-02,Campaign B,15"
        )
        with patch('requests.get', return_value=mock_response):
            result = read_csv_from_url(['date', 'campaign', 'clicks', 'nonexistent_column'])
            self.assertTrue('error' in result)
            self.assertIn('not in index', result['error'])

    def test_failed_fetch(self):
        """
        Test handling of failed data fetching (404 status code).
        """
        mock_response = MagicMock()
        mock_response.status_code = 404
        with patch('requests.get', return_value=mock_response):
            result = read_csv_from_url(['date', 'campaign', 'clicks'])
            self.assertTrue('error' in result)
            self.assertEqual(result['error'], 'Failed to fetch data. Status code: 404')

    def test_exception_handling(self):
        """
        Test handling of exceptions raised during data fetching.
        """
        with patch('requests.get', side_effect=Exception("Test exception")):
            result = read_csv_from_url(['date', 'campaign', 'clicks'])
            self.assertTrue('error' in result)
            self.assertIn('Exception occurred: Test exception', result['error'])

if __name__ == '__main__':
    unittest.main()
