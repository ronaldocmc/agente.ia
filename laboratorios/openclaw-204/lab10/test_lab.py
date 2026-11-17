from policy import Policy
from pathlib import Path
p=Policy(); data=Path('SKILL.md').read_text(); assert p.run('alice','submit',{'id':'SK-1','kind':'skill','body':data,'source':'local:SKILL.md'})['ok']
assert not p.run('alice','read',{'id':'SK-1'})['ok']; assert p.run('carol','approve',{'id':'SK-1','version':1})['ok']
assert p.run('alice','read',{'id':'SK-1'})['body']==data
assert p.run('carol','revise',{'id':'SK-1','body':data+'\nRevisao 2'})['ok']; assert not p.run('alice','read',{'id':'SK-1'})['ok']
assert not p.run('carol','approve',{'id':'SK-1','version':1})['ok']; assert p.run('carol','approve',{'id':'SK-1','version':2})['ok']
print('PASS: skill staging, review, versioning, stale approval')
