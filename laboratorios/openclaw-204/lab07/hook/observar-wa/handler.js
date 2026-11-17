import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const exec=promisify(execFile);
export default async function handler(event){
  if(event.type!=='message'||event.action!=='received')return;
  const c=event.context||{}, m=c.metadata||{};
  if(c.channelId!=='whatsapp'||!c.messageId||typeof c.content!=='string')return;
  // Dedicated DM-only lab account; fail closed on missing canonical sender.
  const sender=m.senderE164;
  if(typeof sender!=='string'||!/^\+[1-9]\d{7,14}$/.test(sender))return;
  if(!/^(FONTE |SOLICITAR |CONSULTAR |RASCUNHO |REVISAR |APROVAR |REJEITAR |PUBLICAR )/.test(c.content))return;
  if(!process.env.OBS_TOKEN)return;
  try{
    const r=await fetch('http://127.0.0.1:8765/mensagem',{method:'POST',headers:{'Content-Type':'application/json',Authorization:'Bearer '+process.env.OBS_TOKEN},body:JSON.stringify({sender,message_id:String(c.accountId||'default')+':'+sender+':'+c.messageId,text:c.content}),signal:AbortSignal.timeout(5000)});
    if(!r.ok)return;
    const result=await r.json();
    if(result.text.startsWith('NEGADO: remetente'))return;
    const args=['message','send','--channel','whatsapp','--target',sender,'--message',result.text];
    if(c.accountId)args.push('--account',c.accountId);
    await exec('openclaw',args,{timeout:15000});
  }catch{console.error('[observar-wa] backend or delivery failed');}
}
