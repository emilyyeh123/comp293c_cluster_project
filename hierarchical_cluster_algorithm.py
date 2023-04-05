import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.cluster.hierarchy as shc
#from sklearn.cluster import AgglomerativeClustering
from sklearn.decomposition import PCA

def main():
    matrixBegin = 0
    geneExpArr = []

    print("Opening File")
    txtFile = open("dupe_fibroblast_data/GSE202991_series_matrix.txt", "r")

    for line in txtFile:
        if matrixBegin == 0 and line == "!series_matrix_table_begin\n":
            # check if matrix begin
            matrixBegin = 1
        elif line == "!series_matrix_table_end\n":
            # check if matrix end
            break

        if matrixBegin == 1 and line != "!series_matrix_table_begin\n":
            rowVals = line.split()
            geneExpArr.append(rowVals)

    txtFile.close()

    print("Creating Dataframe")
    df = pd.DataFrame(geneExpArr)
    colHeaders = df.iloc[0].tolist()[1:]
    rowHeaders = df.iloc[:,0].tolist()[1:]
    geneExpArr = geneExpArr[1:]
    geneExpArr = [i[1:] for i in geneExpArr]
    df = df.drop(columns = df.columns[0])
    df = df.drop(df.index[0])
    #print("\n\n", type(df.iloc[0]), "\n", type(df.iloc[:,0]), "\n\n\n")
    #print("\n\n", df.iloc[0].tolist()[1:], "\n", df.iloc[:,0].tolist()[1:], "\n\n\n")
    df = pd.DataFrame(geneExpArr, columns = colHeaders, index = rowHeaders) # FINAL DATAFRAME
    print(df.head())

    print("Creating Dendrogram")
    figDendrogram = plt.figure()
    plt.title("Gene Expression Dendrogram")
    dend = shc.dendrogram(shc.linkage(df, method='ward'))
    #plt.axhline(y=6, color='r', linestyle='--') # red dotted line
    plt.savefig("dendrogram.png")
    #plt.show()

    print("Plotting Cluster")
    # Use PCA to reduce to 2 dimensions
    pca = PCA(n_components=2)
    pca_features = pca.fit_transform(df.values)
    pca_df = pd.DataFrame(data=pca_features, columns=['PC1', 'PC2'])
    print(pca_df)

    # plot data
    figPlot = plt.figure()
    plt.plot(pca_df["PC1"], pca_df["PC2"], marker="o", linestyle="", alpha = 0.05)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.savefig("clustering.png")
    #plt.show()

if __name__ == "__main__":
	main()
