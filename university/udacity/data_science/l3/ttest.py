from scipy.stats import ttest_ind
from scipy import stats

rvs1 = stats.norm.rvs(loc=5,scale=10,size=500)
rvs2 = stats.norm.rvs(loc=5,scale=10,size=500)

print(ttest_ind(rvs1, rvs2, axis=0, equal_var=False))