
document.addEventListener('DOMContentLoaded',()=>{
 document.querySelectorAll('.tg-code-label').forEach(label=>{
  const pre=label.nextElementSibling;if(!pre||!pre.matches('pre.tg-code'))return;
  const b=document.createElement('button');b.type='button';b.className='tg-copy';b.textContent='Copiar';
  b.addEventListener('click',async()=>{try{if(!navigator.clipboard||!navigator.clipboard.writeText)throw Error();await navigator.clipboard.writeText(pre.textContent);b.textContent='Copiado';}catch(e){const r=document.createRange();r.selectNodeContents(pre);const s=window.getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selecionado: Ctrl+C';}});label.appendChild(b);
 });
 const list=document.querySelector('.tg-checklist');if(list){const boxes=[...list.querySelectorAll('input[type=checkbox]')];const msg=list.querySelector('.tg-progress');function update(){msg.textContent=boxes.filter(b=>b.checked).length+' de '+boxes.length+' etapas registradas nesta sessão (não persistem ao recarregar).';}boxes.forEach(b=>b.addEventListener('change',update));update();}
});
