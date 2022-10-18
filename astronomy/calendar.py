from itertools import accumulate
# Calendar

def JulianDayfromGregorianDate(year, month, day):
    """
    
    """
    # Fractional days are handled by leapday calculation.
    days_in_year = 365
    # After transform, the year will end with February
    days_in_month = [31, 30, 31, 30, 31, 31, 30, 31, 30, 31, 31, 29]
    months_in_year = len(days_in_month)
    # [31, 61, 92, 122, 153, 184, 214, 245, 275, 306, 337, 366]
    days_acc_this_month = list(accumulate(days_in_month))
    # 1582-10-05 => 1582-08-05 after moving February
    switch_year = 1582
    switch_day = 218
    # -4712-01-01.5 => -4713-11-01.5 after moving February
    epoch_year = -4713
    epoch_day = 307.5
    epoch = epoch_day + epoch_year*days_in_year
    # Clean up any 13+ month dates
    year = year + (month-1) // 12
    month = (month-1) % months_in_year + 1
    # Move February to the end of the year.
    if month <= 2: 
        month += 10
        year -= 1
    else:
        month -= 2
    ordinal_day = days_acc_this_month[month-2] + day
    leapdays = LeapDaysGregorian(epoch_year, year)
    # Add back the leapdays from Julian calendar from beginning of switch_year
    if year == switch_year and ordinal_day <= switch_day:
        leapdays += 10
    return days_in_year*year + ordinal_day + leapdays - epoch
def LeapDaysSinceJulianEpoch(year):
    """
    This function calculates the number of leap days since the Julian Epoch (0000-01-01) to the end of argument year (year-12-31) in in the (non-propeletic) Gregorian calendar. It should always return a positive number, so before the Julian epoch would be the number of leap days that will be added by the time of the epoch.
    
    Notes on the algorithm:
    Using the propeletic Gregorian calendar removes 12 leap years (100, 200, 300, 500, 600, 700, 900, 1000, 1100, 1300, 1400, 1500), but only 10 days were removed in 1582 with the adoption of the Gregorian calendar (in the few places where the Gregorian calendar was adopted). This puts the normal integer division algorithm two days short of the actual calendar. 
    
    The additional one leap day after each Epoch switch adds the leap day for year 0 (which of course wouldn't be added before the 0 epoch.)
    
    Adding a one to the year makes sure you are not measuring the leap day that year (i.e. -0004 should not increment the leap day since we are measuring from -0004-12-31) 
    """
    GregorianEpoch = 1582 # Not a (traditional) leap year/not divisible by 4.
    JulianEpoch = 0
    if year >= GregorianEpoch: # Epoch changed in October of GregorianEpoch
        return year//4 - year//100 + year//400 + 3
    elif year >= JulianEpoch: # There is a leap day in JulianEpoch (0000-02-29)
        return year//4 + 1
    else:
        return abs(year+1) // 4
def LeapDaysGregorian(year1, year2):
    """
    Calculates the number of leap days between two whole years year1-12-31 and year2-12-31 using the Gregorian calendar (which uses the Julian Calendar before 1582).
    """
    if year1^year2 >= 0:
        return abs(LeapDaysSinceJulianEpoch(year1) - LeapDaysSinceJulianEpoch(year2))
    else:
        return LeapDaysSinceJulianEpoch(year1) + LeapDaysSinceJulianEpoch(year2)
def parse_isodate_string(str):
    if str[0]=="-":
        str = str[1:]
        sign = -1
    else:
        sign = 1
    year, month, day = str.split('-')
    return (sign*int(year), int(month), float(day))
if __name__=="__main__":
    almostisoformats = ["2000-01-01.5",
                        "1999-01-01.0",
                        "1987-01-27.0",
                        "1987-06-19.5",
                        "1988-01-27.0",
                        "1988-06-19.5",
                        "1900-01-01.0",
                        "1600-01-01.0",
                        "1600-12-31.0",
                        "837-04-10.3",
                        "-123-12-31.0",
                        "-122-01-01.0",
                        "-1000-07-12.5",
                        "-1000-02-29.0",
                        "-1001-08-17.9",
                        "-4712-01-01.5"]
    actual_julian_day = [2451545.0,
                         2451179.5,
                         2446822.5,
                         2446966.0,
                         2447187.5,
                         2447332.0,
                         2415020.5,
                         2305447.5,
                         2305812.5,
                         2026871.8,
                         1676496.5,
                         1676497.5,
                         1356001.0,
                         1355866.5,
                         1355671.4,
                               0.0]
    greg_date_list = map(parse_isodate_string, almostisoformats)
    years, months, days = zip(*greg_date_list)
    julian_day = list(map(JulianDayfromGregorianDate, years, months, days))
    err = [corr-calc for calc, corr in zip(julian_day,actual_julian_day)]
    # print(*[str(z)+":"+x for x, y, z in zip(almostisoformats, julian_day, err)],sep="\n")
    # print("Leap Days:")
    # print(*list(map(LeapDaysSinceJulianDateEpoch,years)))
    # print("Values:")
    # print(*julian_day, sep="\n")
    print(LeapDaysGregorian(-4713,1581))
    print(LeapDaysGregorian(-4713,1582))
    print(LeapDaysGregorian(-4713,1583))
    
    print("Error in Values:")
    print(*err, sep="\n")

