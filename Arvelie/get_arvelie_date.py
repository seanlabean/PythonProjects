from datetime import datetime

def get_arvelie(incept, print_gregorian=False, print_arvelie=False):
    """
    Uses a numeric to alphabetic dictionary as well as the built-in
    python datetime library to construct the current Arvelie date.
    This script properly handles leap years.

    Inputs:

    incept          - the repository inception date.
    print_gregorian - prints the current gregorian date (default: False)
    print_arvelie   - prints the current arvelie date (default: False)

    Outputs:

    arvelie - arvelie date code (string).
    """
    alphabet = {0:"A", 1:"B", 2:"C", 3:"D", 4:"E", 5:"F", 6:"G", 7:"H", \
                8:"I", 9:"J", 10:"K", 11:"L", 12:"M", 13:"N", 14:"O", \
                15:"P", 16:"Q", 17:"R", 18:"S", 19:"T", 20:"U", 21:"V", \
                22:"W", 23:"X", 24:"Y", 25:"Z", 26:"+"}

    now = datetime.now()
    year = now.year
    month = now.month
    day = now.day
    if(print_gregorian):
        print("Gregorian date: {}-{:02d}-{:02d}".format(year, month, day))


    day_of_year = datetime.now().timetuple().tm_yday - 1
    al_key = day_of_year // 14

    arvelie = "{:02d}{}{:02d}".format(year-incept,
                                      alphabet[al_key],
                                      day_of_year%14)
    if(print_arvelie):
        print("Arvelie date: {}".format(arvelie))
    return arvelie

if __name__ == "__main__":
    incept = int(input("What is your inception year? :: "))
    get_arvelie(incept, print_gregorian=True, print_arvelie=True)
