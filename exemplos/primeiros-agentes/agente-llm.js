'use strict';
// Simulação do plano retornado por LLM. Não há inferência real neste código.
const planoSimulado={ferramenta:'consultar_vagas',argumentos:{curso:'IA'}};
const permitidas=new Set(['consultar_vagas']);
function executar(plano){
  if(!permitidas.has(plano.ferramenta)) return {erro:'ferramenta não autorizada'};
  return {curso:plano.argumentos.curso,vagas:20};
}
console.log(executar(planoSimulado));
if(!executar({ferramenta:'excluir_curso',argumentos:{}}).erro) throw Error('Autorização falhou');

