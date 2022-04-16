import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('Which city would you like to analyze, Chicago, New York or Washington? ').lower()
        if city in CITY_DATA:
            break
        else:
            print('\nInvalid input')

    while True:
        month_filter = input('Would you like to filter by month? Enter yes or no. ').lower()
        if month_filter == 'no':
            month = 'all'
            break
        elif month_filter == 'yes':
            while True:
                month = input('Which month? January, February, March, April, May or June? ').lower()
                if month in ['january', 'february', 'march', 'april', 'may', 'june']:
                    break
                else:
                    print('\nInvalid input')
            break
        else:
            print('\nInvalid input')

    while True:
        day_filter = input('Would you like to filter by day of the week? Enter yes or no. ').lower()
        if day_filter == 'no':
            day = 'all'
            break
        elif day_filter == 'yes':
            while True:
                day = input('What day? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday? ').lower()
                if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                    break
                else:
                    print('\nInvalid input')
            break
        else:
            print('\nInvalid input')


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
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

    popular_month = df['month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    print('Most common month:', months[popular_month - 1].title())

    popular_day = df['day_of_week'].mode()[0]
    print('Most common day of week:', popular_day)

    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most frequent start hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    popular_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station:', popular_start_station)

    popular_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station:', popular_end_station)

    popular_start_end_combo = df.groupby(['Start Station','End Station']).size().nlargest(1)
    print('\nMost frequent combination of start station and end station trip:\n', popular_start_end_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total_time = df['Trip Duration'].sum()
    hours = total_time // 3600
    minutes = (total_time % 3600) // 60
    seconds = (total_time % 3600) % 60
    print('Total travel time: {} hours, {} minutes and {} seconds'.format(hours, minutes, seconds))

    mean_time = df['Trip Duration'].mean()
    hours = int(mean_time // 3600)
    minutes = int((mean_time % 3600) // 60)
    seconds = int((mean_time % 3600) % 60)
    print('Mean travel time: {} hours, {} minutes and {} seconds'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_types = df['User Type'].value_counts()
    print('Counts of user type:\n', user_types)

    try:
        gender_count = df['Gender'].value_counts()
        print('\nCounts of gender:\n', gender_count)
    except KeyError:
        print('\nNo gender data to share.')

    try:
        earliest_birth = int(df['Birth Year'].min())
        print('\nEarliest year of birth:', earliest_birth)

        latest_birth = int(df['Birth Year'].max())
        print('Most recent year of birth:', latest_birth)

        common_birth = int(df['Birth Year'].mode()[0])
        print('Most common year of birth:', common_birth)

    except KeyError:
        print('\nNo birth year data to share.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays 5 lines of raw data."""

    row_from = 0
    row_to = 5
    view_data = input('\nWould you like to see the first 5 rows of the raw data? Yes or No? ').lower()
    if view_data == 'yes':
        while True:
            print(df.iloc[row_from:row_to,:])
            row_from += 5
            row_to += 5
            view_more_data = input('\nWould you like to see 5 more rows? Press "Enter key" for Yes or input No? ').lower()
            if view_more_data == 'no' or row_from > len(df.index):
                print('\nEnd of raw data')
                break


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
