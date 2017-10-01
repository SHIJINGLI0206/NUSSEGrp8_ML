import os,sys
import csv

#-------------------addd your code below------------------------
def format_date():
    with open('kc_house_data.csv') as f_org:
        reader = csv.DictReader(f_org, delimiter=',')
        writer = csv.writer(open('kc_house_data_r.csv','w'))
        writer.writerow(['date', 'bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors',
                         'waterfront', 'view', 'condition','grade', 'sqft_above', 'sqft_basement',
                         'yr_built', 'yr_renovated', 'lat', 'long', 'sqft_living15', 'sqft_lot15','price'])

        for rw in reader:
            writer.writerow([rw['date'][:4], rw['bedrooms'], rw['bathrooms'], rw['sqft_living'], rw['sqft_lot'], rw['floors'],
                             rw['waterfront'], rw['view'], rw['condition'], rw['grade'], rw['sqft_above'], rw['sqft_basement'],
                             rw['yr_built'], rw['yr_renovated'], rw['lat'], rw['long'], rw['sqft_living15'],
                             rw['sqft_lot15'],rw['price']])






if __name__ == '__main__':
    format_date()