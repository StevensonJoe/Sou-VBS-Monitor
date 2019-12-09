#souvbs
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import ctypes
import vbsdata
from datetime import datetime
import time


def start_up():
    # start webdriver and login
    driver = webdriver.Chrome()
    driver.get('https://vbspremium.dpworldsouthampton.com/premium/bookings.aspx')
    driver.find_element_by_id("ctl00_plhContent_PremiumLogin_UserName").send_keys(vbsdata.usern)
    driver.find_element_by_id("ctl00_plhContent_PremiumLogin_Password").send_keys(vbsdata.passw)
    driver.find_element_by_name("ctl00$plhContent$PremiumLogin$LoginButton").click()

    search_for = input("What time slot do you need? (hh:mm) ")
    valid_search = None
    while not valid_search:
        try:
            datetime.strptime(search_for, "%H:%M")
            valid_search = True
        except ValueError as e:
            print(e)
            print("Please format as hh:mm e.g. 05:00")
            search_for = input("What time slot do you need? ")
    return driver, search_for

#slot_container = driver.find_element_by_id("windowGridRows")
def main(driver, search_for):


    slots_available = {}
    for i in range(1,25):
        slot = driver.find_element_by_css_selector(f"#windowGridRows > div:nth-child({i})")
        slot = slot.text.split('\n')
        slot_time = slot[0]
        try:
            slot_empty = slot[1]
        except Exception:
            slot_empty = 0
        try:
            slot_regular = slot[2]
        except Exception:
            slot_regular = 0
        
        slots_available[slot_time] = [slot_empty, slot_regular]
        

    for i in slots_available:


        if search_for in str(i).split()[0]:
            print(i)
            print(f"E: {slots_available[i][1]}")
            print(f"R: {slots_available[i][0]}")
            # Slot Available messagebox
            if int(slots_available[i][0]) == 1:
                is_are = "is"
                slot_plural = ""
            else:
                is_are = "are"
                slot_plural = "s"
            slot_amount = slots_available[i][0]

    if int(slot_amount) > 0:
        ctypes.windll.user32.MessageBoxW(0, f"There {is_are} {slot_amount} slot{slot_plural} available for {search_for}!", "Slot Available", 0x30)





if __name__ == "__main__":
    driver, search_for = start_up()
    while True:
        print(f"\n\nSearching for VBS slots for {search_for}")
        main(driver, search_for)
        time.sleep(30)

        
        