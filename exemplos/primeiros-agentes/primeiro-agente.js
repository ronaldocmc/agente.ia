'use strict';
// Agente reflexivo simples. Estado observado: quantidade de vagas.
const decidir = vagas => vagas === 0 ? 'ALERTAR: sem vagas' : 'INFORMAR: vagas disponíveis';
const observar = () => ({ curso: 'Agentes de IA', vagas: 0 });
const percepcao = observar();
const acao = decidir(percepcao.vagas);
console.log({ percepcao, acao });
if (acao !== 'ALERTAR: sem vagas') throw Error('Decisão inesperada');

