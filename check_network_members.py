import sys
import json
sys.path.append('d:/trienkhaihethong')
from remote_exec import run_command

for net in ['news_frontend_net', 'news_backend_net', 'news_monitoring_net']:
    code, out, _ = run_command(f'docker network inspect {net} --format "{{{{json .Containers}}}}"')
    try:
        parsed = json.loads(out)
        print(f"=== {net} ===")
        for cid, cinfo in parsed.items():
            print(f"  - {cinfo['Name']}: {cinfo['IPv4Address']}")
    except Exception as e:
        print(f"Error parsing {net}: {e}, out={out}")
