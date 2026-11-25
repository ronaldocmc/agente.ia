'use strict';
// Skill didática: função parametrizada e verificável, não runtime OpenClaw.
const catalogo=[{nome:'IA',preco:0,vagas:20},{nome:'Agentes',preco:100,vagas:15}];
function recomendar({orcamento}) {
  return catalogo.filter(c=>c.preco<=orcamento&&c.vagas>0);
}
const resultado=recomendar({orcamento:80});
console.log(resultado);
if(resultado.some(c=>c.preco>80||c.vagas<1)) throw Error('Violação de restrição');

