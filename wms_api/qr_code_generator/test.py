import os
import sys
import unittest
from datetime import datetime
from enum import Enum, auto

sys.path.insert(1, os.getcwd()[: -len("test")] + "src")

from qr_code_generator import QrDTO, QrGenerator


#  QRCodeBuilder


class TestSectorTypes(Enum):
    sector1 = auto()
    sector2 = auto()
    sector3 = auto()
    sector4 = auto()
    sector5 = auto()

    @classmethod
    def get_sector_types(self) -> list:
        return [self.sector1, self.sector2, self.sector3, self.sector4, self.sector5]


class TestQrCodeGeneratorTypes(unittest.TestCase):
    qrDTO = QrDTO(
        user_id=1,
        start_date=datetime.now(),
        end_date=datetime.now(),
        start_time="00:00:00",
        end_time="00:00:00",
        sector="sector1",
        package_number=256,
    )

    def test_user_id(self):
        self.assertIsInstance(self.qrDTO.user_id, int)

    def test_start_end_date(self):
        self.assertIsInstance(self.qrDTO.start_date, datetime)
        self.assertIsInstance(self.qrDTO.end_date, datetime)

    def test_start_end_time(self):
        self.assertIsInstance(self.qrDTO.start_time, str)
        self.assertIsInstance(self.qrDTO.end_time, str)

    def test_package_number(self):
        self.assertIsInstance(self.qrDTO.package_number, int)


qr_dto = QrDTO(
    user_id=1,
    start_date=datetime.now(),
    end_date=datetime.now(),
    start_time="00:00:00",
    end_time="00:00:00",
    sector="sector1",
    package_number=256
)
qr = QrGenerator().generate(qr_dto)
print(qr)

if __name__ == "__main__":
    unittest.main()
