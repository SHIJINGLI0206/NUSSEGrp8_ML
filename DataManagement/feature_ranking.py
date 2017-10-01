import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

from sklearn.feature_selection import RFE, f_regression
from sklearn.linear_model import (LinearRegression, Ridge, Lasso, RandomizedLasso)
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestRegressor


class FeatureRanking():
    def __init__(self, fname):
        self.data = fname

    def do_rank(self):
        house = pd.read_csv(self.data)
        house.head()

        #dropping the id and date columns
        house = house.drop(['date'], axis=1)

        str_list = []
        for colname, colvalue in house.iteritems():
            if type(colvalue[1]) == str:
                str_list.append(colname)

        num_list = house.columns.difference(str_list)

        house_num = house[num_list]

        Y = house.price.values
        house = house.drop(['price'],axis=1)
        X = house.as_matrix()
        colnames = house.columns

        ranks = {}
        def ranking(ranks, names, order=1):
            minmax = MinMaxScaler()
            ranks = minmax.fit_transform(order*np.array([ranks]).T).T[0]
            ranks = map(lambda x:round(x,2),ranks)
            return dict(zip(names,ranks))

        rlasso = RandomizedLasso(alpha=0.04)
        # long time
        rlasso.fit(X,Y)
        ranks["rlasso/Stability"] = ranking(np.abs(rlasso.scores_),colnames)
        print('finished')

        lr = LinearRegression(normalize=True)
        lr.fit(X,Y)

        rfe = RFE(lr,n_features_to_select=1, verbose=3)
        rfe.fit(X,Y)
        ranks["RFE"] = ranking(list(map(float,rfe.ranking_)),colnames,order=-1)

        #Using linear regression
        lr = LinearRegression(normalize=True)
        lr.fit(X,Y)
        ranks["LinReg"] = ranking(np.abs(lr.coef_), colnames)

        #using Ridge
        ridge = Ridge(alpha=7)
        ridge.fit(X,Y)
        ranks['Ridge'] = ranking(np.abs(ridge.coef_),colnames)

        #using lasso
        lasso = Lasso(alpha=0.05)
        lasso.fit(X,Y)
        ranks["Lasso"] = ranking(np.abs(lasso.coef_),colnames)

        # long time
        rf = RandomForestRegressor(n_jobs=-1, n_estimators=50, verbose=3)
        rf.fit(X,Y)
        ranks["RF"] = ranking(rf.feature_importances_,colnames)

        r = {}
        for name in colnames:
            r[name] = round(np.mean([ranks[method][name]
                                     for method in ranks.keys()]),2)

        methods = sorted(ranks.keys())
        ranks["Mean"] = r
        methods.append("Mean")

        meanplot = pd.DataFrame(list(r.items()), columns=['Feature', 'Mean Ranking'])

        meanplot = meanplot.sort_values('Mean Ranking', ascending=False)

        sns.factorplot(x='Mean Ranking', y='Feature',data=meanplot, kind='bar', size=4, aspect=1.9, palette='coolwarm')
        plt.savefig('..\\Images\\feature_ranking.jpg')
        #plt.show()

