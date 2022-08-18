## Initial Setup

### TOKENS
SECRETS and TOKENS in .env

LINE_CHANNEL_ACCESS_TOKEN=
LINE_CHANNEL_SECRET=
DEEPL_API_KEY=
WOLFRAM_KEY=

### Deploy
```
python app.py
ngrock http 5000
```
use ngrock temporarily

After getting the ngrock deployed url, set the url/callback to the callback url in LINE Messaging API setting on LINE Platform