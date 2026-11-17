from policy import Policy
from pathlib import Path
p=Policy(); x={'id':'OBS-1','kind':'news','body':'Noticia <teste>','source':'fixture:1'}
assert not p.run('unknown','submit',x)['ok']; assert p.run('alice','submit',x)['ok']
assert not p.run('alice','approve',{'id':'OBS-1','version':1})['ok']; assert not p.run('ed','publish',{'id':'OBS-1','version':1})['ok']
assert p.run('carol','approve',{'id':'OBS-1','version':1})['ok']; assert '&lt;teste&gt;' in p.run('ed','publish',{'id':'OBS-1','version':1})['html']
assert p.run('carol','revise',{'id':'OBS-1','body':'Revisao'})['ok']; assert not p.run('ed','publish',{'id':'OBS-1','version':1})['ok']; assert not p.run('ed','publish',{'id':'OBS-1','version':2})['ok']
assert not p.run('alice','submit',dict(x,id='OBS-2',body='FAKE_SECRET_123'))['ok']
assert not p.run('alice','submit',dict(x,role='editor'))['ok']; assert p.db.execute('SELECT count(*) FROM audit WHERE allowed=0').fetchone()[0]>=7
print('PASS: identity, schema, RBAC, revision, escaping, audit')
