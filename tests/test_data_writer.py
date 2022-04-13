from unittest.mock import patch, mock_open

from data_writer.data_writer import DataWriter


class TestDataWriter:

    @patch('builtins.open', new_callable=mock_open)
    def test_write_location_data(self, mock_open_file):
        writer = DataWriter(file_extension='jsonl')
        writer.write_location_data(file_name='test', data=[{}])
        mock_open_file.assert_called_with('test.jsonl', 'w')
