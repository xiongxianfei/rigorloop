#!/usr/bin/env python3
"""Project current CLI contracts and selected REM methods into customer skills."""
from __future__ import annotations
import argparse
import hashlib
import re
from pathlib import Path, PurePosixPath

ROOT=Path(__file__).resolve().parents[1]
CORE=('route','requirement-analysis','requirement-review','system-design','architecture-design','design-review','plan','delivery-review','implement','code-review','verify')
SUPPORT=('bugfix','explore','learn','research','ci-maintenance','pr')
REM_SOURCES={
 'requirement-analysis':('methods/requirement-analysis.md','methods/scenario-analysis.md','methods/5w2h.md','models/requirements.md','models/scenarios.md','models/system-design.md'),
 'requirement-review':('models/requirements.md','models/scenarios.md','models/system-design.md','methods/requirement-analysis.md'),
 'system-design':('methods/functional-analysis.md','models/system-design.md','models/requirements.md'),
 'architecture-design':('methods/architecture-design.md','methods/architecture-allocation.md','methods/architecture-views.md','methods/5w2h.md','models/architecture-design.md','models/requirements.md'),
 'design-review':('models/system-design.md','models/architecture-design.md','models/requirements.md','methods/architecture-views.md'),
 'plan':('methods/plan-and-assess-verification.md','methods/validate-stakeholder-outcomes.md','concepts/assurance.md','models/README.md','practices/WORKED-EXAMPLE.md'),
 'verify':('methods/plan-and-assess-verification.md','methods/validate-stakeholder-outcomes.md','concepts/assurance.md','models/README.md','practices/verify-and-validate-a-bounded-slice.md','practices/WORKED-EXAMPLE.md'),
}

# A split procedure/model remains complete in every distribution that selects it.
REM_PARTS={
 'models/architecture-design.md':('models/architecture-allocation.md','models/architecture-boundaries.md','models/architecture-realization.md','models/operational-support.md'),
 'models/system-design.md':('models/operational-support.md',),
 'models/README.md':('models/operational-support.md',),
 'methods/architecture-design.md':('methods/realization-design.md',),
 'methods/architecture-views.md':('methods/view-presentation.md','methods/views/logical.md','methods/views/process.md','methods/views/development.md','methods/views/physical.md','methods/views/scenario.md'),
}
for skill, sources in tuple(REM_SOURCES.items()):
    REM_SOURCES[skill]=tuple(dict.fromkeys(source for parent in sources for source in (parent,*REM_PARTS.get(parent,()))))
for skill in ('requirement-analysis','system-design','architecture-design'):
    REM_SOURCES[skill]+=('practices/engineer-a-change.md','practices/WORKED-EXAMPLE.md')

REM_SOURCES['architecture-design']+=('practices/make-an-architecture-decision.md',)

GENERATED_REM_PREFIX='<!-- Generated from rem/'

def destination(source: str) -> str:
    parts=PurePosixPath(source).parts
    return 'rem-'+'-'.join(parts)

def projected_rem(source: str, selected: tuple[str,...]) -> bytes:
    path=ROOT/'rem'/source
    raw=path.read_bytes()
    text=raw.decode('utf-8')
    def link(match):
        label,target=match.groups()
        if target.startswith(('https:','http:','#')):return match.group(0)
        base,separator,anchor=target.partition('#')
        resolved=(path.parent/base).resolve()
        try:relative=resolved.relative_to(ROOT/'rem').as_posix()
        except ValueError:return match.group(0)
        if relative in selected:return f'[{label}]({destination(relative)}{separator}{anchor})'
        return f'[{label}](https://github.com/xiongxianfei/rigorloop/blob/main/rem/{relative}{separator}{anchor})'
    text=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',link,text)
    return (f'<!-- Generated from rem/{source}; source SHA-256 {hashlib.sha256(raw).hexdigest()}. Edit the owning REM source. -->\n\n'+text).encode()

def outputs():
    for name in CORE+SUPPORT:
        root=ROOT/'skills'/name/'references'
        yield root/'operational-recording.md',(ROOT/'templates/shared/operational-recording.md').read_bytes()
        for schema in ('targeted-recording-v2.schema.json','rigorloop-records-v4.schema.json'):
            yield root/schema,(ROOT/'schemas'/schema).read_bytes()
        for source in REM_SOURCES.get(name,()):yield root/destination(source),projected_rem(source,REM_SOURCES[name])

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    errors=[]
    expected={path for path,_ in outputs()}
    for name in CORE+SUPPORT:
        root=ROOT/'skills'/name/'references'
        for path in root.glob('rem-*.md'):
            if path not in expected and path.read_text().startswith(GENERATED_REM_PREFIX):
                if args.check:errors.append(str(path.relative_to(ROOT))+' (obsolete generated resource)')
                else:path.unlink()
    for target,data in outputs():
        if args.check:
            if not target.is_file() or target.read_bytes()!=data:errors.append(str(target.relative_to(ROOT)))
        else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
    if errors:raise SystemExit('Stale or missing operational guidance: '+', '.join(errors))
    print('Operational guidance projections are current.' if args.check else 'Projected current operational guidance.')
if __name__=='__main__':main()
