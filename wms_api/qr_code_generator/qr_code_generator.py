import os
from datetime import datetime
import qrcode

class QrDTO:
    def __init__(
            self,
            user_id: int,
            start_date: datetime,
            end_date: datetime,
            start_time: str,
            end_time: str,
            sector: str,
            package_number: int,
    ):
        self.user_id: int = user_id
        self.start_date: datetime = start_date
        self.end_date: datetime = end_date
        self.start_time: str = start_time
        self.end_time: str = end_time
        self.sector: str = sector
        self.package_number: int = package_number

    def __str__(self):
        return (
                "User ID: "
                + str(self.user_id)
                + "\n"
                + "Start date: "
                + str(self.start_date)
                + "\n"
                + "End date: "
                + str(self.end_date)
                + "\n"
                + "Start time: "
                + self.start_time
                + "\n"
                + "End time: "
                + self.end_time
                + "\n"
                + "Sector: "
                + self.sector
                + "\n"
                + "Package Number: "
                + str(self.package_number)
                + "\n"
        )


# class QRCodeBuilder:
#     def __init__(self, qr_data: QrDTO):
#         self.data = self.generate_data(qr_data)
#
#     def generate_data(self, qr_data: QrDTO):
#         qr_data.user_id = 1,
#         qr_data.start_date = datetime.now(),
#         qr_data.end_date = datetime.now(),
#         qr_data.start_time = "00:00:00",
#         qr_data.end_time = "00:00:00",
#         qr_data.sector = "sector1",
#         qr_data.package_number = 256,
#         return qr_data


class QrGenerator:
    def generate(self, qrDTO):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S_")
        image_name = str(now) + "id" + str(qrDTO.user_id) + ".png"
        img = qrcode.make(qrDTO.__str__())
        img.save(
            os.path.abspath(os.getcwd() + "qr").replace("\\", "/")
            + "/"
            + image_name
        )
        return (
                os.path.abspath(os.getcwd() + "qr").replace("\\", "/")
                + "/"
                + image_name
        )
