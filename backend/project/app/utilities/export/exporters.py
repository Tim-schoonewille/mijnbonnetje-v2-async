from abc import ABC, abstractmethod

from app import models


class Exporter(ABC):
    @abstractmethod
    def export(self, receipts: list[models.ReceiptForExport]) -> None:
        pass


class JSONExporter(Exporter):
    def export(self, receipts: list[models.ReceiptForExport]) -> None:
        print("Exporting to JSON...")


class PDFExporter(Exporter):
    def export(self, receipts: list[models.ReceiptForExport]) -> None:
        print("Exporting to PDF...")


class ImageExporter(Exporter):
    def export(self, receipts: list[models.ReceiptForExport]) -> None:
        print("Exporting images...")
