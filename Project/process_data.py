import pandas as pd

def processData(SH):
    # Formatting the 'endTime' and 'msPlayed' columns
    SH["end-Time"]= pd.to_datetime(SH["endTime"])
    SH['year'] = pd.DatetimeIndex(SH["end-Time"]).year
    SH['month'] = pd.DatetimeIndex(SH["end-Time"]).month
    SH['day'] = pd.DatetimeIndex(SH["end-Time"]).day
    SH['weekday'] = pd.DatetimeIndex(SH["end-Time"]).weekday
    SH['time'] = pd.DatetimeIndex(SH["end-Time"]).time
    SH['hours'] = pd.DatetimeIndex(SH["end-Time"]).hour
    SH['day-name'] = SH["end-Time"].apply(lambda x: x.day_name())
    SH['month-name']= SH['end-Time'].dt.month_name()
    SH['Count'] = 1
    SH["duration (hh-mm-ss)"] = pd.to_timedelta(SH["msPlayed"], unit='ms')
    # This function converts milliseconds to hours
    def hours(x):
        return x.seconds/3600
    # This function converts milliseconds to minutes
    def minutes(x):
        return (x.seconds/60)%60
    SH["Duration(Hours)"] = SH["duration (hh-mm-ss)"].apply(hours).round(2)
    SH["Duration(Minutes)"] = SH["duration (hh-mm-ss)"].apply(minutes).round(2)
    SH.drop(columns=["endTime","duration (hh-mm-ss)","msPlayed"], inplace=True)
    return SH