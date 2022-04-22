import requests
import json
import pandas as pd

## Specify Output File Name as ".csv"
filename = 'example.csv'

## Using Curl from Growjo
url = "https://growjo.com/api/companies/city"

querystring = {"order":"asc","orderBy":"cityRanking","city":"Austin","offset":"0","rowsPerPage":"1000","citypage":"0"}

payload = ""
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "auth": "Basic Z3Jvd2pvQXBpVXNlcjpqazYhNVo5UHViQi5Idlo=",
    "Connection": "keep-alive",
    "Referer": "https://growjo.com/city/Austin/",
    "Cookie": "ezoadgid_333975=-1; ezoref_333975=google.com; ezosuibasgeneris-1=f59b21d5-40a7-4c66-6831-292865e32727; ezoab_333975=mod63; lp_333975=https://growjo.com/city/Austin; ezovuuidtime_333975=1650606742; ezovuuid_333975=92082ce9-2e87-4faf-747d-eccf5233c6a9; ezopvc_333975=2; landingPage=/city/Austin; ezux_lpl_333975=1650606662467|8f843f4b-d82d-4b3d-4f76-1f15d46c7e95|false; ezux_et_333975=55; ezux_tos_333975=76; ezux_ifep_333975=true",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "TE": "trailers"
}

response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

info = json.loads(response.text)

## Dataframe Loading

df = pd.DataFrame(columns=['Rank','Name','Industry','Total Funding','Revenue (M)','Employees', 'Employees (Last)', 'Employee Growth (%)','URL', 'LinkedIn'])
t_list = []

for n in range (500):
    t_list = []
    number = n
    # Company Entry
    company = info['data'][number]
    #Rank
    t_list.append(company['cityRanking'])
    
    #Name
    t_list.append(company['company_name'])
    
    #Industry
    t_list.append(company['industry'])
    
    #Total Funding
    t_list.append(company['total_funding'])
    
    #Revenue
    revenue = str(company['estimated_revenues'])
    revenue = revenue[:-6] + "." + revenue[-6:]
    revenue = revenue[0:5]
    try:
        revenue = float(revenue)
        revenue = round(revenue, 1)
        t_list.append(revenue)
    except ValueError:
        t_list.append(revenue)
    
    #Employees- Presently
    employee_cur = company['current_employees']
    t_list.append(company['current_employees'])
    
    #Employees- Last
    employee_past = company['last_employees']
    t_list.append(company['last_employees'])
    
    #Employee Growth
    employee_growth = ((employee_cur - employee_past)/(employee_past))*100
    employee_growth = round(employee_growth, 3)
    t_list.append(employee_growth)
    
    #URL
    t_list.append(company['url'])
    
    #LinkedIn
    t_list.append(company['linkedin_url'])
    
    #Append df
    df = df.append(pd.Series(t_list, index=df.columns[:len(t_list)]), ignore_index=True)

df.to_csv(filename, index=False)
