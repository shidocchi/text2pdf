# text2pdf
text typesetter


## INSTALL

```
$ python -m pip install git+https://github.com/shidocchi/text2pdf.git
```

## USAGE

```
usage: python -m text2pdf ...

text typesetter

options:
  -h, --help            show this help message and exit
  --raw                 suppress stdin encoding
  --out OUT             output filename
  --page {a3,b4,a4,b5,a5,hagaki}
                        page size
  --landscape           landscape
  --margin MARGIN       margin mm
  --size SIZE           font pt
  --height HEIGHT       line height pt
  --font {cons,yu,noto,udev,ipa}
                        font
  --do {print,edit,open}
                        operation
  --sample              sample text
```

```
$ cat sample.txt | python -m text2pdf
```
