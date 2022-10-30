import os

from jaque import LoadString
from exceptions import JsonException


def good_check_1(content):
    if content.get('name') != 'catalyn45':
        return False

    activities = content.get('activities')
    if len(activities) != 2:
        return False

    if not content.get('male'):
        return False

    return True


def good_check_2(content):
    if len(content) != 2:
        return False

    if content[0].get('product_id') != 1050:
        return False

    if type(content[1]) is not list:
        return False

    return True


def good_check_3(content):
    if type(content) is not list:
        return False

    if content[0].get('guid') != '62abfdf2-e1d6-470e-9430-a00080504383':
        return False

    if content[1].get('tags')[1] != 'magna':
        return False

    if content[1].get('friends')[0].get('name') != 'Ewing Church':
        return False

    return True


def good_check(nr, content):
    try:
        parsed = LoadString(content)
    except JsonException as e:
        print(str(e))
        return False

    if nr == 1:
        return good_check_1(parsed)

    if nr == 2:
        return good_check_2(parsed)

    if nr == 3:
        return good_check_3(parsed)


def main():
    for i in range(1, 4):
        good_content = open(f"./test_jsons/good/test_{i}.json").read()
        if good_check(i, good_content):
            print(f"test {i} good PASSED")
        else:
            print(f"test {i} good FAILED")

        bad_content = open(f"./test_jsons/bad/test_{i}.json").read()

        try:
            LoadString(bad_content)
        except JsonException:
            print(f"test {i} bad  PASSED")
        else:
            print(f"test {i} bad  FAILED")


main()
