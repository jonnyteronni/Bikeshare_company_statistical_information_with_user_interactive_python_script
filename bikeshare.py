import sys
import time
import pandas as pd
from colorama import Fore, Back, init




CITY_DATA = {'chicago': 'chicago.csv',
              'ny': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ['january','february','march','april','may','june']
days = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']



def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all months" to apply no month filter
        (str) day - name of the day of week to filter by, or "all days" to apply no day filter
    """

    # resets colorama on every new print statement
    init(autoreset=True)

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    month = None
    day = None

    print('\nI can share with you really cool information about Chicago, NY and Washington cities.\n')

    while city not in CITY_DATA:
        city = input('\nWhich one do you want to see first?\n').lower()
        if city not in CITY_DATA:
            print('\nThat was a mistake. You wrote ' + Fore.RED + Back.WHITE + '{}'.format(city) + Fore.RESET + Back.RESET + ' instead of writing one of the city\'s names: Chicago, NY or Washington.\n')
            repeat_answer()

    if city == 'ny':
        city = 'new_york_city'

    # get user input for applying filter or not
    while True:
        time_filter = input('\nWould you like to apply a time filter to data?(yes/no)?\n').lower()
        if time_filter == 'no':
            break
        elif time_filter != 'yes':
            print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(time_filter) + Fore.RESET + Back.RESET + '.\n')
            repeat_answer()

        elif time_filter == 'yes':

            # Understands if user wants to filter by month
            while True:
                question = input('Do you want to filter by month?(yes/no)\n').lower()
                if question == 'no':
                        break
                elif question != 'yes':
                    print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(question) + Fore.RESET + Back.RESET + '.\n')
                    repeat_answer()
                else:
                    while True:
                        month = input('\nWhat specific month would you like to have access to? (january, february, ... , june)\n').lower()
                        if month not in months:
                            print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(month) + Fore.RESET + Back.RESET + '.\n')
                            repeat_answer()
                        else:
                            print('\nYou have chosen {}.\n'.format(month))
                            break
                    break

            # Understands if user wants to filter by week day
            while True:
                question = input('Do you want to filter by week day? (yes/no)\n').lower()
                if question == 'no':
                        break
                elif question != 'yes':
                    print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(question) + Fore.RESET + Back.RESET + '.\n')
                    repeat_answer()
                else:
                # get user input for day of week (all, monday, tuesday, ... sunday)
                    while True:
                        day = input('\nWhat specific week day would you like to have access to? (monday, tuesday, ...)\n').lower()
                        print(day)
                        if day not in days:
                            print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(day) + Fore.RESET + Back.RESET + '.\n')
                            repeat_answer()
                        else:
                            print('\nYou have chosen {}.\n'.format(day))
                            break
                    break

            break

    print('-'*40)
    return city, month, day


def repeat_answer():
    """
    Loop that lets user decide if he/she wants to repeat an answer or wants to leave program.

    Args:
        None
    Returns:
        exit program if required by user
    """

    while True:
        repeat = input('Do you want to try again? (yes/no)\n').lower()
        if repeat == 'no':
            print('I\'m sad to see you go but life is full of bad choices so I understand. Bye and see you soon!\n')
            sys.exit()
        elif repeat != 'yes':
            print('\nYou wrote ' + Fore.RED + Back.WHITE + '{}'.format(repeat) + Fore.RESET + Back.RESET + ' instead of yes or no. No problem, you can try the times you want :)\n')
        else:
            break



def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by
        (str) day - name of the day of week to filter by
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city + '.csv')
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # Create new columns with weekday and month
    df['Start Hour'] = df['Start Time'].dt.hour
    df['Weekday'] = df['Start Time'].dt.weekday
    df['Month'] = df['Start Time'].dt.month

    #Filter dataframe with month or weekday if applicable
    if month != None:
        df = df[(df.Month == (months.index(month)+1))]
    if day != None:
        df = df[(df.Weekday == days.index(day))]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('Month: {}'.format(months[df['Month'].mode()[0]-1]).title())

    # display the most common day of week
    print('Weekday: {}'.format(days[df['Weekday'].mode()[0]-1]).title())

    # display the most common start hour
    print('Start hour: {}H'.format(df['Start Hour'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print('Start station: {}'.format(df['Start Station'].mode()[0]).title())

    # display most commonly used end station
    print('End station: {}'.format(df['End Station'].mode()[0]).title())

    # display most frequent combination of start station and end station trip
    df['Concat Stations'] = df['Start Station'] + ' - ' + df['End Station']
    print('Combination: {}'.format(df['Concat Stations'].mode()[0]).title())
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time: {} days {}'.format(int(df['Trip Duration'].sum()/60/60/24),time.strftime('%H Hours %M Minutes %S Seconds',time.gmtime(df['Trip Duration'].sum()))))

    # display mean travel time
    print('Mean travel time: {}'.format(time.strftime('%H Hours %M Minutes %S Seconds',time.gmtime(df['Trip Duration'].mean()))))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types\n')
    print(df.groupby('User Type')['User Type'].count())

    if city == 'washington':
        print('There is no information regarding user gender or birth year for Washington city. We are sorry for the inconvenience.')
    else:
        # Display counts of gender
        print('\nCount of gender types\n')
        print(df.groupby('Gender')['Gender'].count())

        # Display earliest, most recent, and most common year of birth
        print('\nEarliest year of birth: {}'.format(int(df['Birth Year'].min())))
        print('\nMost recent year of birth: {}'.format(int(df['Birth Year'].max())))
        print('\nMost common year of birth: {}'.format(int(df['Birth Year'].mode()[0])))
        print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays 5 rows of raw data for the times user requires."""

    first_row = 0
    last_row = 4
    data_request = input('\nWould you like to see 5 rows of data? (yes or no)\n')
    while True:
        if data_request == 'no':
            break
        elif data_request != 'yes':
            print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(data_request) + Fore.RESET + Back.RESET + '.\n')
            repeat_answer()
        else:
            print(df.iloc[first_row:last_row])
            first_row = last_row + 1
            last_row += 5
            data_request = input('\nWould you like to see more 5 rows of data? (yes or no)\n')

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)
        raw_data(df)
        while True:
            restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
            if restart == 'no':
                sys.exit()
            elif restart != 'yes':
                print('\nCould not understand your choice ' + Fore.RED + Back.WHITE + '{}'.format(restart) + Fore.RESET + Back.RESET + '.\n')
                repeat_answer()
            else:
                break

if __name__ == "__main__":
	main()
