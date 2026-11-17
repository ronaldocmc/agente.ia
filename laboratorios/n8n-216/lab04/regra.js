function avaliar(p){if(p.kind!=='text')return {status:'ignorado'};if(p.sender!=='teste-01')return {status:'negado'};const m=/^ESTOQUE (P\d{3})$/i.exec(p.text||'');return !m?{status:'invalido'}:m[1].toUpperCase()==='P001'?{status:'ok',estoque:8}:m[1].toUpperCase()==='P002'?{status:'ok',estoque:0}:{status:'nao_encontrado'};}
if(typeof module!=="undefined")module.exports=avaliar;
