from pathlib import Path
import hashlib,json,zipfile
r=Path(__file__).resolve().parents[1];archive=r.parent/(r.name+'.zip')
if archive.exists():raise FileExistsError('Refusing to overwrite existing archive: '+str(archive))
qa=json.loads((r/'TESTS/results/final_delivery_QA.json').read_text());assert not qa['preservation']['changed_or_missing']
assert qa['STEP']['all_solids_match_native'] and qa['native']['invalid_geometric_features']==[]
items=[]
for p in sorted(r.rglob('*')):
 if p.is_file() and p.name!='manifest.sha256':items.append((p.relative_to(r).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest()))
manifest=r/'manifest.sha256'
with manifest.open('x',encoding='utf-8') as f:f.write('\n'.join(h+'  '+n for n,h in items)+'\n')
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(r.rglob('*')):
  if p.is_file():z.write(p,p.relative_to(r.parent).as_posix())
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 for name,h in items:assert hashlib.sha256(z.read(r.name+'/'+name)).hexdigest()==h,name
 digest=hashlib.sha256(archive.read_bytes()).hexdigest()
 with archive.with_suffix('.zip.sha256').open('x',encoding='utf-8') as f:f.write(digest+'  '+archive.name+'\n')
 print(json.dumps({'archive':str(archive),'bytes':archive.stat().st_size,'members':len(z.infolist()),'manifest_checked_files':len(items),'CRC':'PASS','archived_SHA256_match':'PASS','archive_SHA256':digest,'prior_files_unchanged':qa['preservation']['prior_files_checked']},indent=2))
