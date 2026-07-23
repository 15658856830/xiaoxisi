import subprocess, json, base64, os

files = subprocess.check_output(['git', 'ls-files'], text=True).strip().split('\n')
print(f'Total files to upload: {len(files)}')

for f in files:
    path = os.path.join(os.getcwd(), f)
    if not os.path.isfile(path):
        print(f'  [skip] not found: {f}')
        continue
    
    with open(path, 'rb') as fp:
        content_b64 = base64.b64encode(fp.read()).decode()
    
    escaped_path = f.replace('\\', '/')
    api_url = f'repos/15658856830/xiaoxisi/contents/{escaped_path}'
    payload = json.dumps({
        'message': 'Initial commit',
        'content': content_b64,
        'branch': 'master'
    })
    
    result = subprocess.run(
        ['gh', 'api', '--method', 'PUT', api_url, '--input', '-'],
        input=payload, capture_output=True, text=True, cwd=os.getcwd()
    )
    
    if result.returncode == 0:
        print(f'  [OK] {f}')
    else:
        err = result.stderr.strip()[:100]
        print(f'  [FAIL] {f}: {err}')

print('Done')
