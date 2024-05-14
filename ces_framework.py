import pandas as pd
import numpy as np
from datetime import datetime as dt
from datetime import date

#Calculations
def uniqueClientsServed(df):
    return df['Clients Unique Identifier'].nunique()

#Filters
def reportingPerFilter(df, rp_start, rp_end):
    if isinstance(rp_start,str):
        rp_start = dt.strptime(rp_start,'%Y-%m-%d')
    if isinstance(rp_end,str):
        rp_end   = dt.strptime(rp_end,'%Y-%m-%d')

    df = df[(df['Enrollments Project Start Date']<=rp_end) & (pd.isnull(df['Enrollments Project Exit Date']) | (df['Enrollments Project Exit Date'] >= rp_start))]
    return df


def excludeNoSpa(df):
    return df[df['SPA'].notnull()]

def exited_period(df, start_date, pre_end_date):
    return df.loc[(df['Enrollments Project Exit Date'] >= start_date) & (df['Enrollments Project Exit Date'] <= pre_end_date)]

def individuals(df):
    return df[(df['Client Assessments Name'].isin(['Individual CES Assessment','VI-SPDAT Prescreen for Single Adults [V2] OC Custom','Veteran Coordinated Entry Assessment [OC Custom]']))]

# def assessment_filter(df):
#     return df[(df['Client Assessments Name'].isin(['Individual CES Assessment']))]

def referral_period(df, start_date, pre_end_date):
    return df[(df['Referrals Referral Date'] >= start_date) & (df['Referrals Referral Date'] <= pre_end_date)]

def housed_ces(df):
    return df[df['Exit Type'] =='Housed in CES']

def housed_elsewhere(df):
    return df[df['Exit Type'] =='Housed Elsewhere']

def housed(df):
    return df[(df['Exit Type'] =='Housed Elsewhere') | (df['Exit Type'] == 'Housed in CES')]

def not_housed(df):
    return df[(df['Exit Type'] !='Housed Elsewhere') & (df['Exit Type'] != 'Housed in CES')]

def negative_enroll_exit(df):
    return df[(df['Enrollment to Exit']>=1)|(~df['Enrollment to Exit'].isnull())]

def negative_enroll_assess(df):
    return df[(df['Enrollment to Assessment']>=0)]

def negative_assess_referral(df):
    return df[(df['Assessment to Referral']>=0)]

def negative_referral_match(df):
    return df[(df['Referral to Match']>=0)]

def negative_match_exit(df):
    return df[(df['Match to Exit']>=0)]

def add_spas_by_city(df):
    #define SPAs by City
    south_spa=["Aliso Viejo", "Dana Point", "Irvine", "Laguna Beach", "Laguna Hills", "Laguna Niguel", "Laguna Woods", "Lake Forest", "Mission Viejo", "Rancho Santa Margarita", "San Clemente", "San Juan Capistrano", "Unincorporated Orange County – South SPA"]
    central_spa=["Costa Mesa", "Fountain Valley", "Garden Grove", "Huntington Beach", "Newport Beach", "Santa Ana", "Seal Beach", "Tustin", "Westminster", "Unincorporated Orange County – Central SPA"]
    north_spa=["Anaheim", "Brea", "Buena Park", "Cypress", "Fullerton", "La Habra", "La Palma", "Los Alamitos", "Orange", "Placentia", "Stanton", "Villa Park", "Yorba Linda", "Unincorporated Orange County – North SPA"]

    #ices: replace empty or unincorporated Client Assessments Assessment Location with Entry Custom What city were you in immediately prior to entry into this project?
    #df['Client Assessments Assessment Location'].fillna(df['Entry Custom What city were you in immediately prior to entry into this project?'], inplace=True)
    #df.loc[df['Client Assessments Assessment Location']=="Unincorporated Orange County", 'Client Assessments Assessment Location']=df['Entry Custom What city were you in immediately prior to entry into this project?']

    #ices: Calculate SPAs
    df.loc[(df['Entry Custom Which SPA is this household being served in?']=="North SPA"),'SPA'] = 'North'
    df.loc[(df['Entry Custom Which SPA is this household being served in?']=="Central SPA"),'SPA'] = 'Central'
    df.loc[(df['Entry Custom Which SPA is this household being served in?']=="South SPA"),'SPA'] = 'South'

    df['Prior City'] = np.nan
    city_cols = ['Entry Custom What city were you in immediately prior to entry into this project?','Entry Screen Prior City','Client Assessments Assessment Location?','Current Living Situation City']
        # df['Prior City'].fillna(df['Entry Custom What city were you in immediately prior to entry into this project?'], inplace=True)
        # df['Prior City'].fillna(df['Entry Screen Prior City'], inplace=True)
        # df['Prior City'].fillna(df['Client Assessments Assessment Location?'], inplace=True)
        # df['Prior City'].fillna(df['Current Living Situation City'], inplace=True)
    for col in city_cols:
        if col in df.columns:
            df['Prior City'].fillna(df[col], inplace=True)
    df['Prior City'].fillna('Unknown', inplace=True)
    
    # df.loc[df['SPA'].isna() | df['Entry Custom What city were you in immediately prior to entry into this project?'].isin(south_spa),'SPA'] = 'South'
    # df.loc[df['SPA'].isna() | df['Entry Custom What city were you in immediately prior to entry into this project?'].isin(central_spa),'SPA'] = 'Central'
    # df.loc[df['SPA'].isna() | df['Entry Custom What city were you in immediately prior to entry into this project?'].isin(north_spa),'SPA'] = 'North'
    df.loc[df['SPA'].isna() | df['Prior City'].isin(south_spa),'SPA'] = 'South'cro womalio
    df.loc[df['SPA'].isna() | df['Prior City'].isin(central_spa),'SPA'] = 'Central'
    df.loc[df['SPA'].isna() | df['Prior City'].isin(north_spa),'SPA'] = 'North'

    return df
    