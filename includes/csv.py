from typing import List, Dict, Any
import csv
import os


class CSVWriter:
    def __init__(self, filename: str, header: List[str], overwrite: bool = False):
        self._filename: str = filename
        self._header: List[str] = header
        self._total_rows_written: int = 0
        self._total_bytes_written: int = 0
        self._file = None

        if os.path.exists(self._filename):
            if not overwrite:
                raise FileExistsError(f"File '{self._filename}' already exists. Use overwrite=True to overwrite.")
            else:
                self._validate_file_for_overwrite()

        self._file = open(self._filename, mode='w', newline='', encoding='utf-8')
        self._writer = csv.DictWriter(self._file, fieldnames=self._header)
        self._writer.writeheader()
        self._total_bytes_written += self._file.tell()

    def _validate_file_for_overwrite(self) -> None:
        if not self._filename.lower().endswith('.csv'):
            raise ValueError(f"File '{self._filename}' is not a CSV file.")
        with open(self._filename, 'r', encoding='utf-8') as f:
            first_line = f.readline().strip()
            if first_line and not first_line.startswith(','.join(self._header)):
                raise ValueError("Existing file is not empty or has incompatible CSV format.")

    def add_row_via_list(self, row: List[Any]) -> Dict[str, int]:
        if len(row) != len(self._header):
            raise ValueError(f"Row column count mismatch: expected {len(self._header)}, got {len(row)}.")
        self._writer.writerow(dict(zip(self._header, row)))
        self._total_rows_written += 1
        bytes_written = self._file.tell() - self._total_bytes_written
        self._total_bytes_written += bytes_written
        return {
            'rows_written': 1,
            'bytes_written': bytes_written,
            'total_rows_written': self._total_rows_written,
            'total_bytes_written': self._total_bytes_written
        }

    def add_row_via_listdict(self, row: Dict[str, Any]) -> Dict[str, int]:
        if set(row.keys()) != set(self._header):
            raise ValueError(f"Row column names mismatch: expected {set(self._header)}, got {set(row.keys())}.")
        self._writer.writerow(row)
        self._total_rows_written += 1
        bytes_written = self._file.tell() - self._total_bytes_written
        self._total_bytes_written += bytes_written
        return {
            'rows_written': 1,
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
