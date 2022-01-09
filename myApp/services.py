import json
import pickle
import time

from selenium.webdriver.common.by import By

from .models import Profile
from .utils import _create_driver

authorization_url = "https://orioks.miet.ru/user/login"
study_url = "https://orioks.miet.ru/student/student"


def get_cookies(profile: Profile) -> dict:
    result = {
        "msg": "Success",
        "cookies": "",
    }
    driver = _create_driver()
    try:
        driver.get(url=authorization_url)
        time.sleep(3)
        login_input = driver.find_element(By.ID, "loginform-login")
        login_input.clear()
        login_input.send_keys(profile.user.username)
        time.sleep(3)
        password_input = driver.find_element(By.ID, "loginform-password")
        password_input.clear()
        password_input.send_keys(profile.user.password)
        time.sleep(3)

        log_in = driver.find_element(By.ID, "loginbut")
        log_in.click()
        time.sleep(2)

        driver.get(url=study_url)

        time.sleep(2)
        result["cookies"] = pickle.dumps(driver.get_cookies())
        return result
    except Exception as ex:
        print(ex)
        result["msg"] = "Error"
        return result
    finally:
        driver.close()
        driver.quit()


def get_marks(profile: Profile) -> dict:
    result = {
        "msg": "Success",
        "marks": dict()
    }
    driver = _create_driver()
    try:
        marks_dict = dict()
        driver.get(url=authorization_url)
        for cookie in pickle.loads(profile.cookies):
            driver.add_cookie(cookie)

        time.sleep(2)

        driver.refresh()
        driver.get(url=study_url)
        time.sleep(2)

        subjects = driver.find_elements(By.XPATH, "//td[@class='ng-binding']")
        subjects = [sub.text for sub in subjects]

        marks = driver.find_elements(By.XPATH, "//span[@class='grade_3 grade'] | //span[@class='grade_4 grade'] | "
                                               "//span[@class='grade_5 grade'] | //span[@class='grade_1 grade']"
                                               "| //span[@class='grade_2 grade']")
        marks = [m.text for m in marks]

        final_marks = driver.find_elements(By.XPATH, '//div[@class="w46 ng-binding"]')
        final_marks = [f.text for f in final_marks]
        final_marks = final_marks[:len(subjects) + 1]
        for i in range(len(subjects)):
            marks_dict[str(i)] = {
                "subject": subjects[i],
                "mark": marks[i] + " " + final_marks[i]
            }

        result["marks"] = marks_dict
        result["cookies"] = pickle.dumps(driver.get_cookies())
        return result
    except Exception as ex:
        print(ex)
        result["msg"] = "Error"
        return result
    finally:
        driver.close()
        driver.quit()


def check_marks(profile: Profile) -> dict:

    result = {
        "msg": "Success",
        "marks": dict(),
        "changes": list()
    }

    # get old marks
    old_marks = json.loads(profile.marks)

    # get fresh marks
    get_dict = get_marks(profile)
    if get_dict.get("msg") == "Error":
        result["msg"] = "Error"
        return result

    fresh_marks = get_dict.get("marks")
    changes = list()
    if len(old_marks) != len(fresh_marks):
        result["marks"] = fresh_marks
        for k, v in fresh_marks.items():
            changes.append({
                "subject": v.get("subject"),
                "mark": v.get("mark")
            })
        result["changes"] = changes
        return result

    for i in range(len(old_marks)):
        if old_marks[str(i)].get("subject") != fresh_marks[str(i)].get("subject") or \
                old_marks[str(i)].get("mark") != fresh_marks[str(i)].get("mark"):
            changes.append({
                "subject": fresh_marks[str(i)].get("subject"),
                "mark": fresh_marks[str(i)].get("mark")
            })
    result["changes"] = changes
    result["marks"] = fresh_marks
    return result
