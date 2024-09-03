from typing import List, Dict, Any
import csv_writer
import os


class CSVWriter:
    def __init__(self, filename: str, header: List[str]):
        self._filename: str = filename
        self._header: List[str] = header
        self._total_rows_written: int = 0
        self._total_bytes_written: int = 0
        self._file = None

        # Check if the file exists
        file_exists = os.path.exists(self._filename)

        # If file exists, validate headers, else create a new file
        if file_exists:
            self._validate_existing_file()
            self._file = open(self._filename, mode='a', newline='', encoding='utf-8')
        else:
            self._file = open(self._filename, mode='w', newline='', encoding='utf-8')
            self._writer = csv.DictWriter(self._file, fieldnames=self._header)
            self._writer.writeheader()
            self._total_bytes_written += self._file.tell()

    def _validate_existing_file(self) -> None:
        """
        Validate if the existing file has headers matching the provided headers.
        """
        if not self._filename.lower().endswith('.csv'):
            raise ValueError(f"File '{self._filename}' is not a CSV file.")

        with open(self._filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            existing_header = next(reader, None)
            if existing_header is None:
                raise ValueError("Existing CSV file is empty or corrupted.")
            if existing_header != self._header:
                raise ValueError(
                    f"Header mismatch: expected {self._header}, found {existing_header} in the existing file."
                )

    def add_row_via_list(self, rows: List[List[Any]]) -> Dict[str, int]:
        """
        Add multiple rows via a list of lists to the CSV file.
        """
        rows_written = 0
        for row in rows:
            if len(row) != len(self._header):
                raise ValueError(f"Row column count mismatch: expected {len(self._header)}, got {len(row)}.")
            self._writer.writerow(dict(zip(self._header, row)))
            rows_written += 1
        bytes_written = self._file.tell() - self._total_bytes_written
        self._total_rows_written += rows_written
        self._total_bytes_written += bytes_written
        return {
            'rows_written': rows_written,
            'bytes_written': bytes_written,
            'total_rows_written': self._total_rows_written,
            'total_bytes_written': self._total_bytes_written
        }

    def add_row_via_listdict(self, rows: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Add multiple rows via a list of dictionaries to the CSV file.
        """
        rows_written = 0
        for row in rows:
            if set(row.keys()) != set(self._header):
                raise ValueError(f"Row column names mismatch: expected {set(self._header)}, got {set(row.keys())}.")
            self._writer.writerow(row)
            rows_written += 1
        bytes_written = self._file.tell() - self._total_bytes_written
        self._total_rows_written += rows_written
        self._total_bytes_written += bytes_written
        return {
            'rows_written': rows_written,
            'bytes_written': bytes_written,
            'total_rows_written': self._total_rows_written,
            'total_bytes_written': self._total_bytes_written
        }

    def close(self) -> None:
        if self._file and not self._file.closed:
            self._file.close()

    def __del__(self) -> None:
        self.close()

    # Read-only properties
    @property
    def filename(self) -> str:
        return self._filename

    @property
    def header(self) -> List[str]:
        return self._header

    @property
    def total_rows_written(self) -> int:
        return self._total_rows_written

    @property
    def total_bytes_written(self) -> int:
        return self._total_bytes_written
