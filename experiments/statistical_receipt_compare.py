"""Cross-version audit of STAT-001; preserve exact integer draws and tail counts.
16 ULP at scale max(1,|reference|) covers the rounded variance/sqrt, subtraction,
division and maximum chain. This is not a tolerance on counts or probabilities.
Both receipts are also checked against rational calibration moments.
"""
import math
from fractions import Fraction

def close_float(actual,expected):
 if not(math.isfinite(actual) and math.isfinite(expected)):raise AssertionError('nonfinite derived statistic')
 tolerance=16*math.ulp(max(1.0,abs(expected)))
 if abs(actual-expected)>tolerance:raise AssertionError('derived statistic exceeds rounding envelope')
 return abs(actual-expected)/math.ulp(max(1.0,abs(expected)))

def compare(actual,archived):
 for field in ('raw_draws','observed_collision_counts','fixed_width_21','maximum_over_48_widths','seed','calibration_draws','evaluation_draws'):
  if actual[field]!=archived[field]:raise AssertionError('exact receipt mismatch: '+field)
 draws=actual['raw_draws'];n=actual['calibration_draws'];means=[];sd=[]
 for j in range(48):
  values=[row[j] for row in draws[:n]];total=sum(values);square=sum(x*x for x in values)
  mean=Fraction(total,n);var=(Fraction(square)-Fraction(total*total,n))/(n-1)
  means.append(float(mean));sd.append(math.sqrt(float(var)))
 maxima=[max((v-means[j])/sd[j] for j,v in enumerate(row)) for row in draws[n:]]
 reference={'calibration_means':means,'calibration_sample_sd':sd,'evaluation_maxima_z':maxima}
 report={}
 for field,ref in reference.items():
  if len(actual[field])!=len(ref) or len(archived[field])!=len(ref):raise AssertionError('derived array length')
  report[field]={'values':len(ref),'max_actual_reference_scaled_ULP':max(close_float(x,y) for x,y in zip(actual[field],ref)),'max_archived_reference_scaled_ULP':max(close_float(x,y) for x,y in zip(archived[field],ref)),'max_cross_version_scaled_ULP':max(close_float(x,y) for x,y in zip(actual[field],archived[field]))}
 return dict(exact_integer_draws_and_tail_decisions=True,rational_mean_variance_reference=True,derived_rounding_limit_scaled_ULP=16,fields=report)
