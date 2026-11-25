'use strict';
// Workflow determinístico: etapas e condições fixas.
function processarInscricao({vagas,aprovado}) {
  const etapas=['consultar'];
  if(vagas<=0) return {etapas, status:'sem vagas'};
  etapas.push('verificar vagas');
  if(!aprovado) return {etapas,status:'aguardando aprovação'};
  etapas.push('simular inscrição');
  return {etapas,status:'simulada'};
}
console.log(processarInscricao({vagas:2,aprovado:true}));
if(processarInscricao({vagas:0,aprovado:true}).status!=='sem vagas') throw Error('Teste falhou');

