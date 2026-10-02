#!/usr/bin/env python3
"""Prepare local credentials and start the classroom Graph Builder."""
from pathlib import Path
import getpass,secrets,subprocess
root=Path(__file__).resolve().parent
credentials=root/'.env'
if not credentials.exists():
    credentials.write_text('NEO4J_PASSWORD='+secrets.token_urlsafe(18)+'\n')
    credentials.chmod(0o600)
backend=root/'backend/.env'
if not backend.exists():
    key=getpass.getpass('OpenRouter API key (hidden): ').strip()
    if not key or any(c in key for c in ('\n','\r','"',"'",' ')):
        raise SystemExit('Enter a non-empty API key without spaces or quotes.')
    template=(root/'backend/.env.local.example').read_text()
    backend.write_text(template.replace('replace-with-your-openrouter-key',key))
    backend.chmod(0o600)
subprocess.run(['docker','compose','-f','compose.local.yaml','up','-d','--build'],cwd=root,check=True)
print('Open http://127.0.0.1:8081; connect using the instructions in LOCAL-SETUP.md.')
