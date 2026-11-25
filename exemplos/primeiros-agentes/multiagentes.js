'use strict';
// Coordenação determinística de papéis. NÃO usa agentes LLM autônomos.
const catalogo=[{id:'C01',preco:50,vagas:4},{id:'C02',preco:90,vagas:0}];
const orientador=(dados,orcamento)=>dados.filter(x=>x.preco<=orcamento);
const secretaria=(candidatos)=>candidatos.filter(x=>x.vagas>0);
const verificador=(escolhidos)=>escolhidos.every(x=>x.vagas>0);
const proposta=secretaria(orientador(catalogo,100));
console.log({proposta,valido:verificador(proposta)});
if(!verificador(proposta)) throw Error('Verificação falhou');

