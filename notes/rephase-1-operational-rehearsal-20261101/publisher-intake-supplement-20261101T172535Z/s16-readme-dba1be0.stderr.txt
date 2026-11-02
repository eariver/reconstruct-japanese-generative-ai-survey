* Host huggingface.co:443 was resolved.
* IPv6: 2600:9000:282b:4e00:17:b174:6d00:93a1, 2600:9000:282b:e400:17:b174:6d00:93a1, 2600:9000:282b:c400:17:b174:6d00:93a1, 2600:9000:282b:a000:17:b174:6d00:93a1, 2600:9000:282b:6c00:17:b174:6d00:93a1, 2600:9000:282b:ea00:17:b174:6d00:93a1, 2600:9000:282b:5a00:17:b174:6d00:93a1, 2600:9000:282b:e200:17:b174:6d00:93a1
* IPv4: 3.169.5.29, 3.169.5.90, 3.169.5.78, 3.169.5.94
*   Trying [2600:9000:282b:4e00:17:b174:6d00:93a1]:443...
* ALPN: curl offers h2,http/1.1
} [5 bytes data]
* TLSv1.3 (OUT), TLS handshake, Client hello (1):
} [1569 bytes data]
* SSL Trust Anchors:
*   CAfile: /etc/ssl/certs/ca-certificates.crt
*   CApath: /etc/ssl/certs
{ [5 bytes data]
* TLSv1.3 (IN), TLS handshake, Server hello (2):
{ [1210 bytes data]
* TLSv1.3 (IN), TLS change cipher, Change cipher spec (1):
{ [1 bytes data]
* TLSv1.3 (IN), TLS handshake, Encrypted Extensions (8):
{ [19 bytes data]
* TLSv1.3 (IN), TLS handshake, Certificate (11):
{ [3811 bytes data]
* TLSv1.3 (IN), TLS handshake, CERT verify (15):
{ [264 bytes data]
* TLSv1.3 (IN), TLS handshake, Finished (20):
{ [36 bytes data]
* TLSv1.3 (OUT), TLS change cipher, Change cipher spec (1):
} [1 bytes data]
* TLSv1.3 (OUT), TLS handshake, Finished (20):
} [36 bytes data]
* SSL connection using TLSv1.3 / TLS_AES_128_GCM_SHA256 / X25519MLKEM768 / RSASSA-PSS
* ALPN: server accepted h2
* Server certificate:
*   subject: CN=huggingface.co
*   start date: Aug 14 00:00:00 2026 GMT
*   expire date: Feb 27 23:59:59 2027 GMT
*   issuer: C=US; O=Amazon; CN=Amazon RSA 2048 M01
*   Certificate level 0: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
*   Certificate level 1: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
*   Certificate level 2: Public key type RSA (2048/112 Bits/secBits), signed using sha256WithRSAEncryption
*   subjectAltName: "huggingface.co" matches cert's "huggingface.co"
* SSL certificate verified via OpenSSL.
* Established connection to huggingface.co (2600:9000:282b:4e00:17:b174:6d00:93a1 port 443) from 2404:7a81:e0a1:4a00:921b:eff:fef6:acc6 port 43044 
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/raw/dba1be0a40aa45a94ad051997016db3960a90277/README.md
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: huggingface.co]
* [HTTP/2] [1] [:path: /deepseek-ai/DeepSeek-V4.1-Flash/raw/dba1be0a40aa45a94ad051997016db3960a90277/README.md]
* [HTTP/2] [1] [user-agent: Mozilla/5.0 (compatible; SP-publisher-supplement/20261101; bounded-research)]
* [HTTP/2] [1] [accept: */*]
} [5 bytes data]
> GET /deepseek-ai/DeepSeek-V4.1-Flash/raw/dba1be0a40aa45a94ad051997016db3960a90277/README.md HTTP/2
> Host: huggingface.co
> User-Agent: Mozilla/5.0 (compatible; SP-publisher-supplement/20261101; bounded-research)
> Accept: */*
> 
* Request completely sent off
} [5 bytes data]
* TLSv1.3 (IN), TLS handshake, Newsession Ticket (4):
{ [157 bytes data]
< HTTP/2 200 
< content-type: text/plain; charset=utf-8
< content-length: 13110
< date: Sun, 01 Nov 2026 17:27:09 GMT
< etag: "211b83857abd5e8420df3a4f10db1096294227e6"
< x-powered-by: huggingface-moon
< x-request-id: Root=1-6ae7766d-37b2d7241c1e0e6f1f957e03
< ratelimit: "resolvers";r=2999;t=231
< ratelimit-policy: "fixed window";"resolvers";q=3000;w=300
< cross-origin-opener-policy: same-origin
< referrer-policy: strict-origin-when-cross-origin
< access-control-max-age: 86400
< access-control-allow-origin: https://huggingface.co
< vary: Origin
< access-control-expose-headers: X-Repo-Commit,X-Request-Id,X-Error-Code,X-Error-Message,X-Total-Count,ETag,Link,Accept-Ranges,Content-Range,X-Linked-Size,X-Linked-ETag,X-Xet-Hash,RateLimit,RateLimit-Policy
< x-repo-commit: dba1be0a40aa45a94ad051997016db3960a90277
< accept-ranges: bytes
< content-disposition: inline; filename*=UTF-8''README.md; filename="README.md";
< content-security-policy: default-src 'none'; sandbox
< x-cache: Miss from cloudfront
< via: 1.1 7e6e0ba378d5b75b7ffdfdca98c5795c.cloudfront.net (CloudFront)
< x-amz-cf-pop: NRT57-P6
< alt-svc: h3=":443"; ma=86400
< x-amz-cf-id: zqSzEFzLauqOTfIb57eOI-g1iYq7AO-1NFit77FH4bO09vMSbpzPuA==
< strict-transport-security: max-age=31536000
< 
{ [7206 bytes data]
* Connection #0 to host huggingface.co:443 left intact
