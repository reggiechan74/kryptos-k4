# Item 8 numerical-control and serialization preflight

The numerical controls completed before actual K4 scoring. The initial JSON exceeded the frozen 64 MiB saved-payload cap; no model failed or was rejected on that basis. All records are retained losslessly in [controls-initial.json.gz](controls-initial.json.gz), with [exact raw/compressed sizes and hashes](receipt.json). Original start/end timestamps were not captured; recording time is not substituted.

The original runner now streams lossless gzip, preserving every candidate under the unchanged saved-output cap. No cap, model, edit, key or alignment domain was expanded. Fresh timestamped controls must pass before original actual scoring. Planted ambiguity is retained rather than truncated to one answer.
