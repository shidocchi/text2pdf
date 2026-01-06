import io
import os
import re
import sys
import argparse
import yaml
from pathlib import Path
from typing import Iterator
from .pdfbase import FontFace, PdfBase

__version__ = '0.1.1'

class Text2Pdf:
  """text typesetter"""

  def __init__(self, textin=None) -> None:
    self.conf = self.load_conf()
    self.font = self.get_font()
    self.args = self.get_args()
    self.pdf = self.init_pdf()
    if self.args.sample:
      self.set_sample()
    elif textin:
      if not self.args.raw:
        textin = io.TextIOWrapper(textin.buffer, encoding='utf-8')
      self.typeset(textin)

  def load_conf(self) -> dict:
    fpath = Path(__file__).resolve().parent / 'config.yaml'
    with open(fpath, 'r', encoding='utf8') as f:
      conf = yaml.safe_load(f)
    return conf

  def get_args(self) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
      prog='python -m text2pdf',
      description='text typesetter')
    parser.add_argument('--raw', help='suppress stdin encoding',
      action='store_true')
    parser.add_argument('--out', help='output filename')
    parser.add_argument('--page', help='page size',
      choices=self.conf['page'].keys())
    parser.add_argument('--landscape', help='landscape',
      action='store_true')
    parser.add_argument('--margin', help='margin mm',
      type=float)
    parser.add_argument('--size', help='font pt',
      type=float)
    parser.add_argument('--height', help='line height pt',
      type=float)
    parser.add_argument('--font', help='font',
      choices=self.font.keys())
    parser.add_argument('--do', help='operation',
      choices=self.conf['choices']['do'])
    parser.add_argument('--sample', help='sample text',
      action='store_true')
    parser.set_defaults(**self.conf['default'])
    return parser.parse_args()

  def get_font(self) -> dict:
    d = {}
    for key in self.conf['font']:
      for path in self.conf['fontpath']:
        p = Path(os.path.expandvars(path),
                 self.conf['font'][key])
        if p.exists():
          d[key] = p
    return d

  def init_pdf(self) -> PdfBase:
    pdf = PdfBase(
      unit='mm',
      orientation='L' if self.args.landscape else 'P',
      format=tuple(self.conf['page'][self.args.page])
    )
    for key in self.font:
      pdf.add_font(key, '', self.font[key])
    pdf.set_margin(self.args.margin)
    pdf.set_auto_page_break(auto=True, margin=10)
    pdf.set_font(self.args.font, '', self.args.size)
    pdf.add_page()
    return pdf

  def save(self) -> None:
    self.pdf.output(self.args.out)
    if self.args.do:
      os.startfile(self.args.out, operation=self.args.do)

  def typeset(self, textin) -> None:
    sep = self.conf['pagesep']
    for page in self.paginate(textin):
      if page == sep:
        self.pdf.add_page()
      else:
        self.pdf.write(self.args.height, page)

  def paginate(self, textin) -> Iterator[str]:
    sep = self.conf['pagesep']
    page = []
    for line in textin:
      while True:
        part = line.partition(sep)
        page.append(part[0])
        if part[1] == '':
          break
        yield ''.join(page)
        yield sep
        page = []
        line = part[2]
        if not line.rstrip():
          break
    if page:
      yield ''.join(page)

  def set_sample(self):
    data = [
      [(key, None),
       (self.conf['sample'], FontFace(key))]
      for key in self.font]
    with self.pdf.table(col_widths=(2,8), first_row_as_headings=False) as table:
      row = table.row()
      row.cell(self.conf['sample_title'], colspan=2)
      for drow in data:
        row = table.row()
        for dcol,style in drow:
          row.cell(dcol, style=style)
