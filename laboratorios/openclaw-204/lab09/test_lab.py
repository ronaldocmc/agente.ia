from policy import Policy
from pathlib import Path
p=Policy('memory-lab.sqlite'); p.db.execute('DELETE FROM items'); p.db.execute('DELETE FROM audit'); p.db.commit()
assert p.run('alice','submit',{'id':'MEM-1','kind':'memory','body':'Fonte verificada sobre agentes','source':'fixture:obs-1'})['ok']
assert p.search('alice','agentes')==[]
assert not p.run('alice','approve',{'id':'MEM-1','version':1})['ok']
assert p.run('carol','approve',{'id':'MEM-1','version':1})['ok']
assert p.search('alice','agentes')[0]['source']=='fixture:obs-1'
p.db.close(); p=Policy('memory-lab.sqlite'); assert len(p.search('alice','agentes'))==1
assert p.run('carol','revise',{'id':'MEM-1','body':'Nova fonte'})['ok']; assert not p.search('alice','fonte')
print('PASS: persistence, provenance, review, role, revision')
