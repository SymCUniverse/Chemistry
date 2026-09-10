#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import system3_clean_ru0001_numerical_v1 as base

SCHEMA='h-ru0001-clean-surface-layer-extension-protocol-v0.3'
STATUS='FROZEN_BEFORE_L15_L17_L19_EXTENSION_RESULTS'


def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20), b''):
            h.update(b)
    return h.hexdigest()


def load(path: str|Path) -> dict[str,Any]:
    row=json.loads(Path(path).read_text())
    if not isinstance(row,dict): raise SystemExit(f'MECHANICAL_HOLD: JSON object required: {path}')
    return row


def write(path: str|Path,row:dict[str,Any]):
    Path(path).parent.mkdir(parents=True,exist_ok=True)
    Path(path).write_text(json.dumps(row,indent=2,sort_keys=True)+'\n')


def contract(protocol_path: Path, source_path: Path) -> tuple[dict[str,Any],dict[str,Any]]:
    p=load(protocol_path); s=load(source_path)
    if p.get('schema')!=SCHEMA or p.get('status')!=STATUS: raise SystemExit('SCIENTIFIC_HOLD: extension protocol not frozen')
    src=p['source_evidence']
    if sha256(source_path)!=src['sha256'] or s.get('status')!=src['required_status']: raise SystemExit('MECHANICAL_HOLD: source layer evidence identity mismatch')
    if s['source_run']['result_file_sha256']!=src['source_result_sha256']: raise SystemExit('MECHANICAL_HOLD: source result hash mismatch')
    f=p['frozen_numerical_settings']; sr=s['reference']
    for k in ('a_angstrom','c_angstrom','bulk_energy_ev_per_atom','ecutwfc_ry','ecutrho_ry','selected_total_vacuum_angstrom','tolerance_ev_per_surface_atom'):
        mapk={'selected_total_vacuum_angstrom':'total_vacuum_angstrom','tolerance_ev_per_surface_atom':'absolute_surface_excess_tolerance_ev_per_surface_atom'}.get(k,k)
        if float(sr[k])!=float(f[mapk]): raise SystemExit(f'SCIENTIFIC_HOLD: frozen source setting drift: {k}')
    if sr['selected_kmesh']!=f['surface_kmesh']: raise SystemExit('SCIENTIFIC_HOLD: kmesh drift')
    b=p['extension_batch']
    if b['source_layers']!=[5,7,9,11,13] or b['new_layers']!=[15,17,19] or b['combined_ladder']!=[5,7,9,11,13,15,17,19] or int(b['terminal_reference_layers'])!=19: raise SystemExit('SCIENTIFIC_HOLD: layer extension ladder drift')
    if float(f['absolute_surface_excess_tolerance_ev_per_surface_atom'])!=0.001: raise SystemExit('SCIENTIFIC_HOLD: 1 meV threshold drift')
    if any(bool(v) for v in p['evidence_firewall'].values()): raise SystemExit('SCIENTIFIC_HOLD: evidence firewall opened')
    if p['provenance']['scientific_settings_changed'] is not False or p['provenance']['thresholds_changed'] is not False: raise SystemExit('SCIENTIFIC_HOLD: provenance drift')
    return p,s


def verify_runtime(p:dict[str,Any], pw:Path, pseudo_dir:Path):
    ru=pseudo_dir/'Ru.nc.pbe.z_16.oncvpsp4.sg15.v0.upf'
    if sha256(pw)!=p['runtime_identity']['pw_x_sha256']: raise SystemExit('MECHANICAL_HOLD: pw.x hash mismatch')
    if not ru.is_file() or sha256(ru)!=p['runtime_identity']['ru_pseudo_sha256']: raise SystemExit('MECHANICAL_HOLD: Ru pseudo hash mismatch')


def run_layer(args):
    pp=Path(args.protocol).resolve(); sp=Path(args.source_evidence).resolve(); p,s=contract(pp,sp)
    layer=int(args.layers)
    if layer not in p['extension_batch']['new_layers']: raise SystemExit('SCIENTIFIC_HOLD: unregistered extension layer')
    pw=Path(args.pw).resolve(); pseudo=Path(args.pseudo_dir).resolve(); verify_runtime(p,pw,pseudo)
    f=p['frozen_numerical_settings']; out=Path(args.out).resolve(); out.mkdir(parents=True,exist_ok=True)
    tag=f'slab_L{layer}_V15_K16_16_1_extension'
    txt=base.slab_input(float(f['a_angstrom']),float(f['c_angstrom']),layer,float(f['total_vacuum_angstrom']),int(f['ecutwfc_ry']),int(f['ecutrho_ry']),tuple(f['surface_kmesh']),pseudo,'__OUTDIR__',tag)
    row=base.execute_qe(out,pw,txt,int(p['execution']['per_layer_timeout_seconds']),tag)
    gamma=(float(row['energy_ev'])-layer*float(f['bulk_energy_ev_per_atom']))/2.0
    cell_z,_=base.slab_geometry(float(f['a_angstrom']),float(f['c_angstrom']),layer,float(f['total_vacuum_angstrom']))
    row.update({'schema':'h-ru0001-layer-extension-case-v0.1','status':'VALID_EXTENSION_LAYER','layers':layer,'surface_excess_ev_per_surface_atom':gamma,'total_vacuum_angstrom':float(f['total_vacuum_angstrom']),'cell_z_angstrom':cell_z,'kmesh':list(f['surface_kmesh']),'ecutwfc_ry':int(f['ecutwfc_ry']),'ecutrho_ry':int(f['ecutrho_ry']),'protocol_sha256':sha256(pp),'source_evidence_sha256':sha256(sp),'scientific_settings_changed':False,'thresholds_changed':False,'paid_compute_used':False})
    path=out/f'SYSTEM3_LAYER_L{layer}_RESULT.json'; write(path,row); print(json.dumps(row,indent=2,sort_keys=True)); print(f'SYSTEM3_LAYER_L{layer}_VALID')


def adjudicate(args):
    pp=Path(args.protocol).resolve(); sp=Path(args.source_evidence).resolve(); p,s=contract(pp,sp)
    roots=Path(args.results_root).resolve(); combined=[]
    for r in s['layer_measurements']:
        combined.append({'layers':int(r['layers']),'surface_excess_ev_per_surface_atom':float(r['surface_excess_ev_per_surface_atom']),'source':'v3_source'})
    for layer in p['extension_batch']['new_layers']:
        hits=list(roots.rglob(f'SYSTEM3_LAYER_L{layer}_RESULT.json'))
        if len(hits)!=1: raise SystemExit(f'MECHANICAL_HOLD: expected one L{layer} extension result, found {len(hits)}')
        r=load(hits[0])
        if r.get('status')!='VALID_EXTENSION_LAYER' or int(r.get('layers',0))!=layer: raise SystemExit(f'MECHANICAL_HOLD: L{layer} result identity mismatch')
        if r.get('protocol_sha256')!=sha256(pp) or r.get('source_evidence_sha256')!=sha256(sp): raise SystemExit(f'MECHANICAL_HOLD: L{layer} provenance hash mismatch')
        if r.get('scientific_settings_changed') is not False or r.get('thresholds_changed') is not False: raise SystemExit(f'SCIENTIFIC_HOLD: L{layer} reports drift')
        combined.append({'layers':layer,'surface_excess_ev_per_surface_atom':float(r['surface_excess_ev_per_surface_atom']),'energy_ev':float(r['energy_ev']),'input_sha256':r['input_sha256'],'output_sha256':r['output_sha256'],'elapsed_s':float(r['elapsed_s']),'source':'extension_v1'})
    combined.sort(key=lambda x:x['layers'])
    expected=p['extension_batch']['combined_ladder']
    if [r['layers'] for r in combined]!=expected: raise SystemExit('MECHANICAL_HOLD: combined layer ladder incomplete')
    tol=float(p['frozen_numerical_settings']['absolute_surface_excess_tolerance_ev_per_surface_atom']); ref=combined[-1]['surface_excess_ev_per_surface_atom']
    deltas=[abs(r['surface_excess_ev_per_surface_atom']-ref) for r in combined]
    selected=None
    for i,r in enumerate(combined[:-1]):
        if r['layers']<int(p['frozen_numerical_settings']['minimum_eligible_layers']): continue
        if all(d<=tol for d in deltas[i:]): selected=r['layers']; break
    passed=selected is not None
    result={'schema':'h-ru0001-clean-surface-layer-extension-result-v0.3','status':p['decision']['pass_status'] if passed else p['decision']['hold_status'],'next_gate':p['decision']['pass_next_gate'] if passed else p['decision']['hold_next_gate'],'selected_layers':selected,'terminal_reference_layers':combined[-1]['layers'],'terminal_surface_excess_ev_per_surface_atom':ref,'tolerance_ev_per_surface_atom':tol,'combined_layers':combined,'deltas_to_terminal_ev_per_surface_atom':deltas,'next_batch_if_hold':None if passed else p['decision']['next_batch_if_hold'],'source_result_sha256':p['source_evidence']['source_result_sha256'],'source_evidence_sha256':sha256(sp),'protocol_sha256':sha256(pp),'scientific_settings_changed':False,'thresholds_changed':False,'kinetic_inputs_used':False,'chi_used':False,'paid_compute_used':False}
    write(args.out,result); print(json.dumps(result,indent=2,sort_keys=True)); print(result['status'])


def self_test(args):
    p,s=contract(Path(args.protocol).resolve(),Path(args.source_evidence).resolve())
    rows=[{'layers':7,'surface_excess_ev_per_surface_atom':1.0000},{'layers':9,'surface_excess_ev_per_surface_atom':1.0004},{'layers':11,'surface_excess_ev_per_surface_atom':1.0002}]
    i,d=base.suffix_selection(rows,0.001,eligible=lambda r:r['layers']>=7)
    assert i==0 and max(d)<=0.001
    rows2=[{'layers':7,'surface_excess_ev_per_surface_atom':1.0000},{'layers':9,'surface_excess_ev_per_surface_atom':1.0030},{'layers':11,'surface_excess_ev_per_surface_atom':1.0002}]
    i2,_=base.suffix_selection(rows2,0.001,eligible=lambda r:r['layers']>=7)
    assert i2 is None
    print('SYSTEM3_LAYER_EXTENSION_SELF_TEST_PASS')
    print('NEW_LAYERS=15,17,19')
    print('TOLERANCE_EV_PER_SURFACE_ATOM=0.001')
    print('NEXT_BATCH_IF_HOLD=21,23,25')


def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest='cmd',required=True)
    x=sub.add_parser('self-test'); x.add_argument('--protocol',required=True); x.add_argument('--source-evidence',required=True); x.set_defaults(func=self_test)
    x=sub.add_parser('run-layer'); x.add_argument('--protocol',required=True); x.add_argument('--source-evidence',required=True); x.add_argument('--layers',type=int,required=True); x.add_argument('--pw',required=True); x.add_argument('--pseudo-dir',required=True); x.add_argument('--out',required=True); x.set_defaults(func=run_layer)
    x=sub.add_parser('adjudicate'); x.add_argument('--protocol',required=True); x.add_argument('--source-evidence',required=True); x.add_argument('--results-root',required=True); x.add_argument('--out',required=True); x.set_defaults(func=adjudicate)
    a=ap.parse_args(); a.func(a)
if __name__=='__main__': main()
