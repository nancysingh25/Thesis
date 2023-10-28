
"""
This function is written to analysis of the RMSD,GDT AND LGA scores
reads the excel file with data and then generates the Graph for each of the scoring matrix
When RMSD data is analyized then sheet_name was "RMSD" for GDT it was "GDT" and for LGA
it was "LGA"
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#reads the data from excel file
df = pd.read_excel("C:/Users/HP/Desktop/Thesis/results.xlsx", sheet_name="LGA", engine='openpyxl')
#plots the data from the excel file
gfg = sns.lineplot(data=df[['Modeller', 'PHYRE2', 'ITASSER']])
gfg.set_xlabel("Protein",fontsize=13)
gfg.set_ylabel("LGA score",fontsize=13)
# gfg.set(xticks=(range(1, 19)))
gfg.set_xticks(range(len(df)))
gfg.set_xticklabels(labels=range(1, 21))
plt.show()
