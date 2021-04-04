# text-and-log-counter

learning how to use `collections.Counter` and regex in python for count words in txt file or ips/status codes in server access log.

## features
- `text` mode: lowercase words, remove punctuation, show top N words
- `log` mode: parse ip address, request path, and http status code from access logs
- handle missing file and weird encoding without crashing
- optional `--json-out` save report
