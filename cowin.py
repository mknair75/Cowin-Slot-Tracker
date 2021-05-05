import winsound
import requests
from tabulate import tabulate
import pandas  as pd
from timeloop import Timeloop
from datetime import timedelta, datetime

loop_interval = 300
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 60000  # Set Beep Duration To 1000 ms == 1 second
pin = '560076'  # Location pin where you are planning to register for vaccine
district = '265'
#district = '294'
#district = '296'
current_time = datetime.now()
today = current_time.strftime('%d-%m-%Y')
# Cowin API path
cowin_pin = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByPin?pincode=" + pin + "&" + "date=" + today
cowin_dist = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=" + district + "&" + "date=" + today
tl = Timeloop()

def query_cowin():
    pd.set_option('display.max_columns', None)
    #r = requests.get(cowin_pin)
    r = requests.get(cowin_dist)
    data = r.json()
    df = pd.json_normalize(data, 'centers')
    return df
    # print(tabulate(df[['name', 'fee_type', 'sessions']], headers='keys', tablefmt='pretty'))


def check_criteria(data):
    found = False
    for index, row in data.iterrows():
        sessions_data = pd.json_normalize(row['sessions'])
        print(row['name'])
        print(tabulate(sessions_data[['date', 'available_capacity', 'min_age_limit', 'vaccine']], headers='keys',
                       tablefmt='psql'))

        for i, srow in sessions_data.iterrows():
            if srow['min_age_limit'] == 18:
                if srow['available_capacity'] > 0:
                    found = True
                    str = srow['vaccine']
                    # if str.startswith("COVI"):
                    #    winsound.Beep(frequency, duration)
                    # winsound.PlaySound("SystemHand", winsound.SND_ALIAS)
    if found == True:
        winsound.Beep(frequency, duration)

# Loop every
@tl.job(interval=timedelta(seconds=loop_interval))
def loopjob():
    daf = query_cowin()
    check_criteria(daf)


if __name__ == "__main__":
    tl.start(block=True)
