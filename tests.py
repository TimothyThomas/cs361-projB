from __future__ import print_function
import requests
import bs4


TOPURL = 'http://52.38.130.134:3000/'
NUM_PASSED = 0
NUM_FAILED = 0

def build_url(route, query):
    return TOPURL + route + query

def test_request(route, query, expected): 
    res = requests.get(build_url(route, query))
    soup = bs4.BeautifulSoup(res.text, "html.parser")
    cells = soup.select('td')
    names = [cell.getText() for cell in cells]
    print("Result of test {}: ".format(route+query), end='') 
    print_result(names, expected, res)


def print_result(actual, expected, res):
    global NUM_PASSED, NUM_FAILED
    if actual == expected:
        print('OK.')
        NUM_PASSED += 1
    else:
        print('FAILED.')
        print('\tExpected: {}'.format(expected))
        print('\tReceived: {}'.format(actual))
        print('\tURL: {}'.format(res.url))
        print('\tStatus Code: {}'.format(res.status_code))
        NUM_FAILED += 1


def main():
    test_request('personbyskill', '?skillName="Magic"', 
            ['Harry', 'Potter', 'Hermione', 'Granger', 'Ronald', 'Weasley'])
    test_request('personbyskill', '?skillName="French"', ['Hermione', 'Granger'])
    test_request('personbyskill', '?skillName="Spanish"', [])
    test_request('locationbyskill', '?skillName="Magic"', ['HW1N', 'Hogworts', 'WC2N', 'London'])
    test_request('locationbyskill', '?skillName="Computer Hacking"', [])
    test_request('skillbysimpleperson', '?fname="Draco"&lname="Malfoy"', [])
    test_request('skillbysimpleperson', '?fname="John"&lname="Doe"', ['Wood working'])
    test_request('skillbydetailedperson', '?dob="1985-01-01"&zipcode="HW1N"&gender="M"', ['Magic'])
    test_request('skillshareByLocation', '?zipCode="12334"', [])
    test_request('skillshareByLocation', '?zipCode="90012"', 
                 ['John', 'Doe', 'Jane', 'Doe', 'Wood working', '90012'])
    test_request('skillshareByLocation', '?zipCode="WC2N"', 
                 ['Hermione', 'Granger', 'Ronald', 'Weasley', 'French', 'WC2N', 
                  'Hermione', 'Granger', 'John', 'Doe', 'Magic', 'WC2N'])
    test_request('skillbylocation', '?zipCode="90012"', 
                 ['Jane', 'Doe', 'C++', 'Jane', 'Doe', 'German'])
    test_request('skillbylocation', '?zipCode="abcde"', []) 

    print("\nTesting complete.  {} passed.  {} failed.".format(NUM_PASSED, NUM_FAILED))


if __name__ == "__main__":
    main()
