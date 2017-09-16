import os,sys
import csv

#-------------------addd your code below------------------------
def format_date():
    with open('org_kc_house_data.csv') as f_org:
        reader = csv.DictReader(f_org, delimiter=',')
        writer = csv.writer(open('pre_kc_house_data.csv','wb'))
        for rw in reader:
            print(rw['date'])




if __name__ == '__main__':
    format_date()