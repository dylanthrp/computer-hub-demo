"""Prepare a local upload directory. This never publishes anything."""
from pathlib import Path
import shutil
from build import main as build

ROOT=Path(__file__).resolve().parents[1]
if __name__=='__main__':
    build()
    output=ROOT/'dist'
    (output/'assets').mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/'index.html',output/'index.html')
    (output/'.nojekyll').write_text('',encoding='utf-8')
    for source in (ROOT/'assets').rglob('*'):
        if source.is_file() and 'originals' not in source.relative_to(ROOT/'assets').parts:
            target=output/'assets'/source.relative_to(ROOT/'assets')
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copy2(source,target)
    print('Prepared local dist/. No publishing or DNS action performed. Review docs/SOURCES.md before launch.')
