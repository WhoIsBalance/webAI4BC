import pandas as pd
from sklearn.metrics import cohen_kappa_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from scipy import stats
import numpy as np


def kappa(brcat_rs, df_rs):

    kappa_val = cohen_kappa_score(brcat_rs, df_rs)
    return kappa_val

def plot_confusion_matrix(cm):

    sns.heatmap(cm, annot=True,
                xticklabels=['low risk', 'high risk'], 
                yticklabels=['low risk', 'high risk'])

    # 添加标题和标签
    plt.title('Confusion Matrix', fontsize=16)
    plt.xlabel('DeepSeek R1-7B-a', fontsize=14)
    plt.ylabel('DS-7B', fontsize=14)

    plt.show()


def Hierarchical_analysis(df, model, factor, c=True):

    df['DS-7B'] = (df['DS-7B'] > 0.5).astype(int)
    df['DS-7B-a'] = (df['DS-7B-a'] > 0.5).astype(int)

    df['first_tide'] = (df['first_tide'] >= 12).astype(int)

    sub_df = df[[factor, model]]
    

    if c == False:
        # 非分类变量
        sub_df_grouped = sub_df.groupby(model)
        data4test = []
        for name, group in sub_df_grouped:
            data4test.append(group.to_numpy().reshape(-1))
        
        statistic, p_value = stats.mannwhitneyu(data4test[0], data4test[1])
        print("statistic:", statistic)
        print("pvalue:", p_value)

    else:
        # 分类变量
        cm = []
        factor_classes = sub_df[model].unique()
        sub_df_grouped = sub_df.groupby(model)
        for name, group in sub_df_grouped:
            group = group.to_numpy().reshape(-1)
            factor_freq = []
            for factor_class in factor_classes:
                factor_freq.append((group == factor_class).sum())
            cm.append(factor_freq)
        
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(cm)
        if (expected < 5).any() or df.shape[0] < 40:
            # 使用Fisher精确检验
            chi2_stat, p_value = stats.fisher_exact(cm)
        print("chi2_stat:", chi2_stat)
        print("pvalue:", p_value)





df = pd.read_excel('D:\ProgramFiles\Hybribio\BreastCancer\data_ds.xlsx')
brcat_rs = df["DS-7B"].to_numpy()
df_rs = df["DS-7B-a"].to_numpy()


brcat_rs = (brcat_rs >0.5).astype(int)
df_rs = (df_rs >0.5).astype(int)

# cm = confusion_matrix(brcat_rs, df_rs)
# print(cm)
# plot_confusion_matrix(cm)
kappa_val = kappa(brcat_rs, df_rs)
print(f"Cohen's Kappa: {kappa_val:.4f}")

print("====================================")

r = pearsonr(df['DS-7B'],df['DS-7B-a'])
print("pearson系数：",r[0])
print("   P-Value：",r[1])


print("====================================")
Hierarchical_analysis(df, 'DS-7B-a', 'family_cancer', c=True)
Hierarchical_analysis(df, 'DS-7B', 'high_calorie', c=True)
