"""Explicit row-choice relation: intelligibility is not a unique inverse."""
from strip_source_gates import AZ,validate_strips,crypt

def candidates(block,strips,allow_plaintext_row=False):
 validate_strips(strips)
 if not block or len(block)>len(strips):raise ValueError('one nonempty partial/full block required')
 rows=range(26) if allow_plaintext_row else range(1,26)
 return [dict(displacement=d,plaintext=crypt(block,strips,0,{0:d},True)) for d in rows]
