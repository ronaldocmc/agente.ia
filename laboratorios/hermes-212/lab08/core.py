"""Consulta determinística: pacote didático; não acessa serviços externos."""
import json
from pathlib import Path
CATALOGO = Path(__file__).with_name('catalogo_sintetico_2026.json')

def consultar_curso(curso: str) -> dict:
    """Retorna exclusivamente os dados de um curso público sintético, por nome ou ID."""
    if not isinstance(curso, str) or not curso.strip() or len(curso) > 120:
        return {'status': 'esclarecer', 'mensagem': 'Informe o nome ou ID do curso.'}
    for item in json.loads(CATALOGO.read_text(encoding='utf-8'))['cursos']:
        if curso.strip().casefold() in (item['nome'].casefold(), item['id'].casefold()):
            return {'status': 'ok', 'curso': item['nome'], 'vagas': item['vagas'],
                    'inscricoes': item['inscricoes'], 'fonte': CATALOGO.name}
    return {'status': 'nao_encontrado', 'mensagem': 'Curso não localizado.', 'fonte': CATALOGO.name}

def atender(acao: str, curso: str = '') -> dict:
    """A fronteira é estrutural: não existe operação de escrita, shell ou rede."""
    if acao == 'consultar':
        return consultar_curso(curso)
    if acao == 'inscrever':
        return {'status': 'esclarecer' if not curso else 'revisao',
                'mensagem': 'Informe o curso e procure o canal autorizado. Nenhuma inscrição foi realizada.'}
    return {'status': 'negado', 'mensagem': 'Operação não autorizada.'}

if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description='Consulta de dados fictícios, sem LLM')
    p.add_argument('acao'); p.add_argument('curso', nargs='?', default='')
    a = p.parse_args()
    print(json.dumps(atender(a.acao, a.curso), ensure_ascii=False, indent=2))
