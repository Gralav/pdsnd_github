import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
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
        try:
            cities = ["chicago", "new york city", "washington"]
            city = input("Enter the name of the city (Chicago, New York City, Washington): ").lower()
            if city not in cities:
                raise ValueError("Invalid city input. Please choose from Chicago, New York City, or Washington")
            months = ["all", "january", "february", "march", "april", "may", "june"]
            month = input("Enter the name of the month (all, January, February, ... June): ").lower()
            if month not in months:
                raise ValueError("Invalid month input. Please choose 'all' or a month from January to June")
            days = ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
            day = input("Enter the name of the day (all, Monday, Tuesday, ... Sunday): ").lower()
            if day not in days:
                raise ValueError("Invalid day input. Please choose 'all' or a day of the week")
            break
        except Exception as e:
            print(str(e))
            print("Please re-enter your inputs.")
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

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Start Time'].dt.month == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Start Time'].dt.weekday_name == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month is: ", df['Start Time'].dt.month.mode()[0])

    # display the most common day of week
    print("The most common day of week is: ", df['Start Time'].dt.weekday_name.mode()[0])

    # display the most common start hour
    print("The most common start hour is: ", df['Start Time'].dt.hour.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most commonly used start station is: ", df['Start Station'].mode()[0])

    # display most commonly used end station
    print("The most commonly used end station is: ", df['End Station'].mode()[0])

    # display most frequent combination of start station and end station trip
    df['Route'] = df['Start Station'] + " to " + df['End Station']
    print("The most frequent combination of start station and end station trip is: ", df['Route'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print("The total travel time is: ", df['Trip Duration'].sum())

    # display mean travel time
    print("The mean travel time is: ", df['Trip Duration'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:\n", df['User Type'].value_counts())

    # Display counts of gender
    try:
        print("\nCounts of gender:\n", df['Gender'].value_counts())
    except KeyError:
        print("Gender data is not available for this city.")

    # Display earliest, most recent, and most common year of birth
    try:
        print("\nThe earliest birth year is: ", int(df['Birth Year'].min()))
        print("The most recent birth year is: ", int(df['Birth Year'].max()))
        print("The most common birth year is: ", int(df['Birth Year'].mode()[0]))
    except KeyError:
        print("Birth year data is not available for this city.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df, response):
    """
    Displays rows of raw data based on user request.

    Args:
        (DataFrame) df - Pandas DataFrame containing city data filtered by month and day
        (str) response - User response to see the raw data.
    """
    index = 0
    while True:
        if response.lower() != 'yes':
            break
        else:
            print(df.iloc[index:index+5])
            index += 5
            response = input("Would you like to see the next 5 rows of data? Enter yes or no: ")
            continue


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # ask user if they want to see 5 lines of raw data
        response = input("\nWould you like to see the raw data? Enter yes or no: ")
        display_raw_data(df, response)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
	
	
