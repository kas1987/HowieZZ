import os, re
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
pages = ['index.html','browse.html','series.html','body.html','character.html',
         'family.html','quiz.html','craft.html','contact.html']
must = ['assets/site.css','assets/site.js','ZX.load(']
print('== structural checks ==')
ok = True
for p in pages:
    fp = os.path.join(root, p)
    if not os.path.exists(fp):
        print('MISSING', p); ok=False; continue
    t = open(fp, encoding='utf-8').read()
    miss = [m for m in must if m not in t]
    # red flags: literal undefined/null rendered, leftover ZX.mountNav present
    flags = []
    if 'ZX.mountNav' not in t: flags.append('no-mountNav')
    if re.search(r'>\s*(undefined|null|NaN)\s*<', t): flags.append('literal-null-in-html')
    size = len(t)
    status = 'OK' if not miss and not flags else 'CHECK'
    if miss or flags: ok=False
    print(f'{status:6} {p:18} {size:6}b  missing={miss} flags={flags}')
print('ALL-STRUCTURE-OK' if ok else 'STRUCTURE-ISSUES')
