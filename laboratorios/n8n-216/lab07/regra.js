function avaliar(p){return {status:!Number.isFinite(p.frequencia)||p.frequencia<0||p.frequencia>100?'invalido':p.frequencia>=70&&p.regular===true?'apto':'nao_apto'};}
if(typeof module!=="undefined")module.exports=avaliar;
