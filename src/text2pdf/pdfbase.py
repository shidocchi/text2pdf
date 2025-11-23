from fpdf import FPDF
from fpdf.fonts import FontFace

class PdfBase(FPDF):
  """PDF writer"""

  def _header(self):
    pass

  def _footer(self):
    pass
