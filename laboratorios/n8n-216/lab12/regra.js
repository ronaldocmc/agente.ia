function avaliar(p){return {status:p.role==='editor'&&p.approved===true&&Number.isInteger(p.version)&&p.version===p.approvedVersion&&typeof p.hash==='string'&&p.hash.length>0&&p.hash===p.approvedHash?'publicacao_autorizada':'negado'};}
if(typeof module!=="undefined")module.exports=avaliar;
