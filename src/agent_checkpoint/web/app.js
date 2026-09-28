/* Offline, read-only rendering. Never place report strings in HTML or Mermaid syntax. */
const $ = selector => document.querySelector(selector);
const params = new URLSearchParams(location.hash.slice(1));
const token = params.get('token') || '';
history.replaceState(null, '', location.pathname);
let selected = null, lastReport = null, lastGood = null, paused = false, busy = false;
let mermaid = '';
function node(tag, text, className) { const item=document.createElement(tag); item.textContent=text; if(className) item.className=className; return item; }
function stamp(value) { return value ? new Date(value).toLocaleTimeString() : 'Timestamp unknown'; }
function seconds(value) { return value === null || value === undefined ? 'duration unknown' : `${value.toFixed(3)} s`; }
function map(report) {
  const events=report.events, route=[...events].reverse().find(e=>e.kind==='route'), checks=events.filter(e=>e.kind==='check');
  const unfinished=checks.some(e=>e.pairing==='finish_not_observed');
  const uncertain=checks.some(e=>['ambiguous','association_unavailable'].includes(e.pairing));
  const complete=report.last_recorded_completion;
  const newer=complete && events.some(e=>e.kind==='check' && e.sequence>complete.sequence);
  const labels={task:report.task_id?'Contract recorded':'Choose a task',route:route?`${route.source==='jev_gateway'?'Jev':'Local routing'}: ${route.status}`:'Routing not observed',check:uncertain?'Check pairing uncertain':unfinished?'Check finish not observed':checks.length?'Check results recorded':'No check events in window',complete:complete?`Recorded ${complete.status}`:'No recorded completion'};
  const observed={task:!!report.task_id,route:!!route,check:checks.length>0,complete:!!complete};
  for(const [key,text] of Object.entries(labels)) { const el=$(`#flow-${key}`); el.textContent=text; el.className=observed[key]?'observed':''; }
  if(unfinished||uncertain) $('#flow-check').classList.add('attention');
  if(newer || complete?.status!=='ready') $('#flow-complete').classList.add('attention');
  $('#decision-note').textContent = `${route?.reason_code ? 'Routing reason: '+route.reason_code+'. ' : ''}${newer?'Check activity was recorded after this completion. ':''}${uncertain?'Some lifecycle associations are ambiguous or unavailable. ':''}${unfinished?'An unmatched start is not proof a process is still running. ':''}Every completion shown is historical; source freshness has not been revalidated.`;
  // Only fixed IDs and a small enum determine diagram highlights; report text cannot inject syntax.
  mermaid='flowchart LR\n  T[Contract recorded] --> R{Routing requested}\n  R -->|Jev selected or none| A[Advisory only]\n  R -->|Skipped or unavailable| A\n  A --> C[Explicit configured checks]\n  C --> D{Evidence reducer}\n  D -->|Required pass| P[Recorded ready]\n  D -->|Required fail| F[Needs changes]\n  D -->|Missing stale or unavailable| U[Unresolved]\n  P --> H[History is not current verification]\n  F --> H\n  U --> H\n';
  if(complete) { const id={ready:'P',needs_changes:'F',unresolved:'U'}[complete.status]; if(id) mermaid+=`  style ${id} fill:#ead891,stroke:#875719\n`; }
  $('#mermaid').textContent=mermaid;
}
function renderTasks(items) {
  const tasks=$('#tasks'), focused=document.activeElement;
  const hadFocus=tasks.contains(focused);
  const old=[...tasks.children], byId=new Map(old.map(button=>[button.dataset.taskId,button]));
  const buttons=items.map(task=>{
    const button=byId.get(task.task_id) || node('button','');
    button.dataset.taskId=task.task_id;
    const label=`${task.task_id.slice(0,12)}… · r${task.contract_revision}`;
    if(button.textContent!==label) button.textContent=label;
    button.title=task.task_id; button.setAttribute('aria-pressed',String(task.task_id===selected));
    button.onclick=()=>{selected=task.task_id; poll();}; return button;
  });
  // Unchanged polls keep DOM identity. A changed order may detach a focused node.
  if(old.length!==buttons.length || old.some((button,index)=>button!==buttons[index])) {
    tasks.replaceChildren(...buttons);
    if(hadFocus) (buttons.includes(focused)?focused:$('#pause')).focus({preventScroll:true});
  }
}
function render(report) {
  renderTasks(report.tasks);
  $('#task-limit').textContent=report.tasks_truncated?'Task list truncated. Use CLI reporting for specific task IDs.':'';
  const identity=report.source_identity;
  $('#identity').textContent=`Viewer ${report.reporter_version} · source ${identity?.role ?? 'unknown'} ${identity?.version ?? ''} (operator declaration, not attestation) · per-event producer identities may be unknown`;
  const completion=report.last_recorded_completion, usage=report.usage;
  $('#verdict').textContent=completion?.status ?? 'Not observed';
  $('#revision').textContent=completion?`Revision ${completion.contract_revision ?? '?'} · not revalidated`:'No completion in returned window';
  $('#calls').textContent=`${usage.physical_requests_known} known${usage.physical_requests_unknown ? ' + unknown' : ''}`;
  $('#reserved').textContent=`Task reservations: ${usage.budget_reserved_calls ?? 'unknown'} · window only`;
  $('#tokens').textContent=`${usage.input_tokens_known} / ${usage.output_tokens_known}`;
  $('#billing').textContent=`Unknown-token decisions: ${usage.input_tokens_unknown} in / ${usage.output_tokens_unknown} out · dollars unknown`;
  $('#checks').replaceChildren();
  for(const check of completion?.required_checks || []) { const row=node('div','', 'row'); const label=node('div',check.id); label.append(node('small',check.reason_code || 'No reason recorded')); row.append(label,node('span',check.status,check.status)); $('#checks').append(row); }
  if(!completion?.required_checks.length) $('#checks').append(node('p','No completion obligations in this window.','muted'));
  $('#actions').replaceChildren();
  for(const action of completion?.next_actions || []) { const row=node('div','', 'row'); const label=node('div',action.kind.replaceAll('_',' ')); label.append(node('small',`${action.reason_code} · ${action.check_ids.join(', ')}`)); row.append(label); $('#actions').append(row); }
  if(!completion?.next_actions.length) $('#actions').append(node('p','No typed actions recorded. Legacy runtimes may not provide them.','muted'));
  for(const detail of completion?.stale_diagnostics || []) {
    const row=node('div','','row'), label=node('div',`Stale evidence: ${detail.check_id}`);
    label.append(node('small',`Context ${detail.context_comparison}${detail.changed_components.length?': '+detail.changed_components.join(', '):''}. Workspace file metadata changed: ${detail.workspace_generation_changed===null?'unknown':detail.workspace_generation_changed?'yes':'no'}. Historical comparison only; no values shown.`));
    row.append(label); $('#actions').append(row);
  }
  $('#window-note').textContent=`${report.events.length} events · ${report.truncated?'TRUNCATED WINDOW':'window not truncated'} · ${report.unavailable_events} unavailable records · ${usage.conflicting_decisions} conflicting decisions`;
  map(report); renderEvents();
}
function renderEvents() {
  if(!lastReport) return;
  const body=$('#events'); body.replaceChildren(); const filter=$('#filter').value;
  const shown=lastReport.events.filter(e=>filter==='all'||e.kind===filter);
  for(const event of [...shown].reverse()) {
    const row=node('tr',''); const description=node('td',event.operation || event.kind);
    description.append(node('small',[event.check_id,event.phase,event.transport,event.producer_version?`producer ${event.producer_version}`:null].filter(Boolean).join(' · ')));
    const outcome=node('td',event.phase==='started'?'Recorded start':event.status || 'unknown',event.status||'unknown');
    const pairing={finish_observed:`Finish observed at #${event.related_sequence}`,start_observed:`Start observed at #${event.related_sequence}`,finish_not_observed:'Finish not observed in this window',start_not_observed:'Start not observed in this window',ambiguous:'Ambiguous lifecycle records',association_unavailable:'Association metadata unavailable'}[event.pairing];
    outcome.append(node('small',pairing || event.reason_code));
    if(event.reason_code && event.phase!=='started' && pairing) outcome.append(node('small',event.reason_code));
    const timing=node('td',stamp(event.recorded_at)); timing.append(node('small',seconds(event.duration_seconds)));
    row.append(node('td',String(event.sequence)),description,outcome,timing); body.append(row);
  }
}
async function poll() {
  if(busy||paused) return; busy=true;
  const requested=selected;
  try {
    if(!token) throw Error('Open the original session URL printed by the dashboard command.');
    const response=await fetch('/api/report?limit=100'+(requested?'&task='+encodeURIComponent(requested):''), {headers:{Authorization:'Bearer '+token},cache:'no-store',signal:AbortSignal.timeout(5000)});
    if(!response.ok) throw Error(`Report unavailable (HTTP ${response.status}).`);
    const report=await response.json();
    if(requested!==selected) return;
    if(!selected && report.tasks.length) { selected=report.tasks[0].task_id; setTimeout(poll,0); return; }
    lastReport=report; lastGood=new Date(); render(report);
    $('#connection').className=''; $('#connection').textContent=`${paused?'Polling paused':'Polling every 2 s'} · last successful read ${lastGood.toLocaleTimeString()} · no execution`;
  } catch(error) {
    $('#connection').className='error'; $('#connection').textContent=`${error.message} ${lastGood?'Showing stale last-good report from '+lastGood.toLocaleTimeString()+'.':'No report loaded.'}`;
  } finally { busy=false; }
}
function download(name,text,type) { const url=URL.createObjectURL(new Blob([text],{type})); const a=node('a',''); a.href=url; a.download=name; a.click(); setTimeout(()=>URL.revokeObjectURL(url),1000); }
$('#pause').onclick=()=>{paused=!paused; $('#pause').textContent=paused?'Resume polling':'Pause polling'; if(paused) $('#connection').textContent='Polling paused. Displayed history is not current readiness.'; else poll();};
$('#filter').onchange=renderEvents;
$('#json').onclick=()=>{if(lastReport) download('checkpoint-history.json',JSON.stringify(lastReport,null,2),'application/json');};
$('#diagram').onclick=()=>{if(mermaid) download('checkpoint-decisions.mmd',mermaid,'text/plain');};
poll(); setInterval(poll,2000);
