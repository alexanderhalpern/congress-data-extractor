import shutil, openpyxl
from datetime import datetime
from models import LLMResult
from utils import row_values


class ExcelWriter:
    def __init__(self, template: str = "in/Oversight.xlsx") -> None:
        self.out_file = f"out/Oversight_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        shutil.copy(template, self.out_file)
        self.wb = openpyxl.load_workbook(self.out_file)
        self.ws_h = self.wb["hearingdata"]
        self.ws_w = self.wb["witnessdata"]
        self.ws_m = self.wb["memberdata"]
        self.h_headers = [c.value for c in self.ws_h[1]]
        self.w_headers = [c.value for c in self.ws_w[1]]
        self.m_headers = [c.value for c in self.ws_m[1]]

    def write(self, result: LLMResult) -> None:
        self.ws_h.append(row_values(result.hearing.model_dump(), self.h_headers))
        for w in result.witnesses:
            self.ws_w.append(row_values(w.model_dump(), self.w_headers))
        for m in result.members:
            self.ws_m.append(row_values(m.model_dump(), self.m_headers))
        self.wb.save(self.out_file)
