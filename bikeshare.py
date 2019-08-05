import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january', 'february', 'march', 'april', 'may', 'june']

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']

## Git Project - Task 4D - Change n.1 
## Git Project - Task 4D - Change n.2 

def get_filters():
    """
    Asks user to specify a city, month and day to analyze.

    Returns:
        (str) city - name of the city to analyze: new york city, washington or chicago
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = str(input('Choose a city (chicago, new york city or washington?): ')).lower()
        except:
            print('That\'s not a valid city name!')
            continue

        if city not in CITY_DATA:
            print('That\'s not a valid city name! Please, choose one of the options above.')
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = str(input('Choose a month (january, february, ..., june or all, to apply no month filter): ')).lower()
        except:
            print('That\'s not a valid month name!')
            continue

        if month not in months and month != 'all':
            print('That\'s not a valid month name! Please, choose one of the options above.')
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = str(input('Choose a day of the week (monday, tuesday, ..., sunday or all, to apply no day filter): ')).lower()
        except:
            print('That\'s not a valid day of the week name!')
            continue

        if day not in days and day != 'all':
            print('That\'s not a valid day of the week name! Please, choose one of the options above.')
            continue
        else:
            break


    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    #choose csv file
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]

    print('Most Frequent Month:', popular_month)

    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]

    print('Most Frequent Day of Week:', popular_day)

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour

    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]

    print('Most Frequent Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]

    print('Most Frequent End Station:', popular_end_station)

    # display most frequent combination of start station and end station trip
    df['Station Combination'] = df['Start Station'] + ' - ' + df['End Station']
    popular_trip = df['Station Combination'].mode()[0]

    print('Most Frequent Trip:', popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()/3600

    print('Total travel time (in hours):', total_time)
    # display mean travel time
    mean_time = df['Trip Duration'].mean()

    print('Mean travel time (in seconds):', mean_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types

    user_types_count = df['User Type'].value_counts()
    print('Counts of user types:\n', user_types_count.index[0], user_types_count[0], '\n', user_types_count.index[1], user_types_count[1])

    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()

        print('Counts of gender:\n', gender_count.index[0], gender_count[0], '\n', gender_count.index[1], gender_count[1])
        # Display earliest, most recent, and most common year of birth
        year_birth_count = df['Birth Year'].value_counts()

        print('Earliest year of birth:', str(year_birth_count.index.min()).split('.')[0])
        print('Most recent year of birth:', str(year_birth_count.index.max()).split('.')[0])
        print('Most common year of birth:', str(year_birth_count.index[0]).split('.')[0])

    else:
        print('There is no Gender and Birth Year data for this city!')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Displays individual trip data."""

    yes_count = 0

    # get user input 'yes' or 'no' to view individual trip data
    while True:
        try:
            show_data = str(input('Would you like to view individual trip data? ')).lower()
        except:
            print('That\'s not a valid city name!')
            continue

        if show_data == 'yes':
            df_display = df.iloc[yes_count*5:yes_count*5+5]
            yes_count += 1
            print(df_display)
            continue
        elif show_data == 'no':
            break
        else:
            print('That\'s not a valid answer! Please, choose "yes" or "no".')
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
