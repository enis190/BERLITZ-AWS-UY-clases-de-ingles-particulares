import boto3, os, time
from pathlib import Path

bucket = "brltz-lp-uy"
prefix = "clases-de-ingles-particulares/"
local = Path(__file__).parent.resolve()

s3 = boto3.client('s3')
keys = []
for page in s3.get_paginator('list_objects_v2').paginate(Bucket=bucket, Prefix=prefix):
    for obj in page.get('Contents', []):
        k = obj['Key']
        if k != prefix and not k.endswith('/'):
            keys.append(k)

print(f"Downloading {len(keys)} files...")
t0 = time.time()
for i, k in enumerate(keys, 1):
    rel = os.path.relpath(k, prefix)
    dest = local / rel
    os.makedirs(dest.parent, exist_ok=True)
    s3.download_file(bucket, k, str(dest))
    if i % 50 == 0:
        print(f"{i}/{len(keys)}")

print(f"Done in {time.time()-t0:.1f}s")
