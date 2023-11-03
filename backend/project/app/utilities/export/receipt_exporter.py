from app import models
from app.utilities.export.exporters import (
    Exporter,
    ImageExporter,
    JSONExporter,
    PDFExporter,
)

exporters = {"pdf": PDFExporter, "json": JSONExporter, "image": ImageExporter}


class ReceiptExporter:
    def __init__(
        self, receipts: list[models.ReceiptForExport], export_types: list[str]
    ) -> None:
        self.receipts = receipts
        self.export_types = export_types
        self.exporters: list[Exporter]
        self.init_exporters()

    def init_exporters(self) -> None:
        self.exporters = [
            exporters[export_type]()
            for export_type in self.export_types
            if export_type in exporters.keys()
        ]

    def export(self) -> None:
        for exporter in self.exporters:
            exporter.export(self.receipts)

        self.exporters = []
