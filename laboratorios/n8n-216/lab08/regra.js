function avaliar(p){let t=String(p.assunto||'').toUpperCase();return {status:t.includes('CERTIFICADO')?'certificado':t.includes('INSCRIÇÃO')?'inscricao':'revisao'};}
if(typeof module!=="undefined")module.exports=avaliar;
