function avaliar(p){const cat={C001:{nome:'Introdução à IA',vagas:30},C002:{nome:'Agentes de IA',vagas:25}}; let r=typeof p.curso==='string'&&Object.hasOwn(cat,p.curso)?cat[p.curso]:undefined;return p.acao!=='consultar'?{status:'negado'}:r?{status:'ok',...r}:{status:'nao_encontrado'};}
if(typeof module!=="undefined")module.exports=avaliar;
