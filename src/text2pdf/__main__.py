import sys
from . import Text2Pdf

if __name__ == '__main__':
  d = Text2Pdf(sys.stdin)
  d.save()
