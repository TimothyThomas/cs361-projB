from __future__ import print_function
import requests
import bs4


TOPURL = 'http://52.38.130.134:3000/'


def test_personbyskill(test_id, skill, expected): 
    """Select all people matching skill."""
    url = TOPURL + 'personbyskill' + '?skillName="{}"'.format(skill)
    res = requests.get(url)

    soup = bs4.BeautifulSoup(res.text, "html.parser")
    cells = soup.select('td')
    names = [cell.getText() for cell in cells]

    print("Result of personbyskill test {}: ".format(test_id), end='') 
    print_result(names, expected, res)


def print_result(actual, expected, res):
    if actual == expected:
        print('OK.')
    else:
        print('FAILED.')
        print('\tExpected: {}'.format(expected))
        print('\tReceived: {}'.format(actual))
        print('\tURL: {}'.format(res.url))
        print('\tStatus Code: {}'.format(res.status_code))



def main():
    test_personbyskill(1, 'Magic', ['Harry', 'Potter', 'Hermione', 'Granger', 'Ronald', 'Weasley'])
    test_personbyskill(2, 'French', ['Hermione', 'Granger'])
    test_personbyskill(3, 'Spanish', ['blah'])


if __name__ == "__main__":
    main()
