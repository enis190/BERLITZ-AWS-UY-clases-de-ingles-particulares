import boto3, os
from pathlib import Path

bucket = "brltz-lp-uy"
prefix = "clases-de-ingles-particulares/"
local = Path(__file__).parent.resolve()

s3 = boto3.client('s3')
total = 0

for root, dirs, files in os.walk(local):
    for file in files:
        local_path = Path(root) / file
        rel_path = local_path.relative_to(local)
        s3_key = prefix + rel_path.as_posix()
        if '.sass-cache' in s3_key:
            continue
        content_type = "text/html" if file.endswith('.html') else \
                       "text/css" if file.endswith('.css') else \
                       "application/javascript" if file.endswith('.js') else \
                       "image/png" if file.endswith('.png') else \
                       "image/svg+xml" if file.endswith('.svg') else \
                       "font/woff2" if file.endswith('.woff2') else \
                       "application/json" if file.endswith('.map') else \
                       "text/plain"
        extra = {'ContentType': content_type}
        s3.upload_file(str(local_path), bucket, s3_key, ExtraArgs=extra)
        total += 1
        if total % 50 == 0:
            print(f"Uploaded {total}")

print(f"Done! {total} files uploaded to s3://{bucket}/{prefix}")
