function avaliar(p){if(p.sender!=='aluno-teste')return {status:'negado'};const m=/^\/curso\s+(C\d{3})$/i.exec(p.text||'');if(!m)return {status:'invalido'};return m[1].toUpperCase()==='C001'?{status:'ok',vagas:30}:{status:'nao_encontrado'};}
if(typeof module!=="undefined")module.exports=avaliar;
