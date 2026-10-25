import json
with open('d:/trienkhaihethong/audit_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for k, v in data.items():
    print(f"\n==================== {k} (exit: {v['exit_code']}) ====================")
    out = v['output'].strip()
    print(out)
    if v['error'].strip():
        print(f"[STDERR]: {v['error'].strip()}")
