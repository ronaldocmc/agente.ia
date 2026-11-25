from comum import consultar_curso
import json
assert json.loads(consultar_curso("C001"))["nome"]=="Banco de Dados"
assert json.loads(consultar_curso(" c002 "))["vagas"]=="15"
assert "erro" in json.loads(consultar_curso("C999"))
print("3 testes da ferramenta: OK")
