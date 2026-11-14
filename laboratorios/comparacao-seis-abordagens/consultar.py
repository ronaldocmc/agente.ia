import sys,json
from regras import consultar_curso
if __name__=='__main__': print(json.dumps(consultar_curso(sys.argv[1] if len(sys.argv)>1 else ''),ensure_ascii=False))
