from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

import os

from random import randrange

from json import load

from openai import OpenAI

options = Options()
options.add_experimental_option("detach", True)

url = 'https://www.mcdvoice.com/'

with open('secrets.json', 'r') as file:
    secrets = load(file)
openai_api_key = secrets["api_key"]

openai_client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_api_key,
)



hashmap_template = {
    "visit_type": ["Carry-out", "Dine-in"], # Drive Thru is built in.
    "member_of_rewards": [["Yes", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr/td[1]/label"], ["No", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr/td[2]/label"]],
    "asked_about_mobile_app": [["Yes", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[1]/label"], ["No", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[2]/label"]],
    "greet_by_name_or_thank": [["Yes", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[1]/label"], ["No", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[2]/label"]],
    "lunch_order": False,
    "additional_order_addons": [["None", "None"], ["McCafe", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[3]/span/span"], ["Desserts", ["/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[4]/span/span"]]],
    "lunch_menu": [
        ["$5 Meal Deal", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[1]/span/span"],
        ["Smokey BLT QPC", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[2]/span/span"],
        ["Double Smokey BLT QPC", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[3]/span/span"],
        ["Big Mac", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[4]/span/span"],
        ["Quarter Pounder Burger", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[5]/span/span"],
        ["McCrispy/McCrispy Deluxe", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[6]/span/span"],
        ["Spicy McCrispy/Spicy McCrispy Deluxe", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[7]/span/span"],
        ["Fish Sandwich", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[8]/span/span"],
        ["McChicken", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[9]/span/span"],
        ["Chicken Nuggets", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[10]/span/span"],
        ["Hamburger/Cheeseburger", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[11]/span/span"],
        ["Fries", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[12]/span/span"],
        ["McDouble/Double Cheeseburger", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[13]/span/span"]
    ],
    "breakfast_menu": [
        ["Muffin Sandwich", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[1]/span/span"],
        ["Biscuit Sandwich", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[2]/span/span"],
        ["McGriddle Sandwich", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[3]/span/span"],
        ["Hotcakes", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[4]/span/span"],
        ["Big Breakfast", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[5]/span/span"],
        ["Burrito", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[6]/span/span"],
        ["Hashbrown", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[7]/span/span"]
    ],
    "mccafe_menu": [
        ["Brewed Coffee", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[1]/span/span"],
        ["Iced Coffee", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[2]/span/span"],
        ["Latte", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[3]/span/span"],
        ["Mocha", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[4]/span/span"],
        ["Macchiato", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[5]/span/span"],
        ["Soft Drink", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[6]/span/span"],
        ["Frozen Drink/Smoothie", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[7]/span/span"],
        ["Iced/Sweet Tea", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[8]/span/span"],
        ["Lemonade", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[9]/span/span"]
    ],
    "dessert_menu": [
        ["Shake", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[1]/span/span"],
        ["Kit Kat Banana Split McFlurry", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[2]/span/span"],
        ["Sundae", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[3]/span/span"],
        ["Cone", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[4]/span/span"],
        ["McFlurry", "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[5]/span/span"]
    ],
    "reccomend_to_others": [["Highly Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[1]/label"],
                            ["Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[2]/label"],
                            ["Somewhat Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[3]/label"]],
    "return_to_this_mcdonalds": [["Highly Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[1]/label"],
                            ["Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[2]/label"],
                            ["Somewhat Likely", "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[3]/label"]]
}

    
def gamble(context: str, context_hashmap: dict) -> str:
    context_list = context_hashmap[context] 
    # len({k: v for k, v in d.items() if not isinstance(v, (dict, list))})
    num_choices = len(context_list)
    choice = randrange(0, num_choices - 1)
    context_hashmap[context] = context_list[choice]
    return context_hashmap[context][1] # return the XPATH of the choice.

def chat_with_gpt(prompt: str):
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="gpt-3.5-turbo-0125",
    )
    return chat_completion.choices[0].message.content
    
def take_survey(survey_code: str, employee_name: str) -> str:
    survey_code = tuple(survey_code.split("-"))
    context_hashmap = hashmap_template.copy()
    employee_name = employee_name
    chromeDriverManager = ChromeDriverManager()
    driver = webdriver.Chrome(service=Service(chromeDriverManager.install()), 
                            options=options)
    driver.get(url)
    driver.implicitly_wait(5)
    
    driver.find_element(By.ID, "CN1").send_keys(survey_code[0])
    driver.find_element(By.ID, "CN2").send_keys(survey_code[1])
    driver.find_element(By.ID, "CN3").send_keys(survey_code[2])
    driver.find_element(By.ID, "CN4").send_keys(survey_code[3])
    driver.find_element(By.ID, "CN5").send_keys(survey_code[4])
    driver.find_element(By.ID, "CN6").send_keys(survey_code[5])
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    driver.find_element(By.ID, "textR000455.1").click() # saying we placed an order with an employee. "2" is kiosk, "3" is mobile app
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    if (survey_code[1].startswith("13")): # it is a drive-thru order.
        context_hashmap["visit_type"] = "Drive-thru"
        elem_id_to_click = "textR004000.2"
        driver.find_element(By.ID, "textR004000.2").click()
    else:
        gamble("visit_type", context_hashmap)
        if (context_hashmap["visit_type"] == "Dine-in"):
            elem_id_to_click = "textR004000.1"
        else:
            elem_id_to_click = "textR004000.3"
    driver.find_element(By.ID, elem_id_to_click).click()
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr/td[1]/label").click()
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    driver.find_element(By.XPATH, gamble("member_of_rewards", context_hashmap)).click() # clicking rewards member or not.
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    # check if we say we were a rewards member:
    driver.find_element(By.XPATH, gamble("asked_about_mobile_app", context_hashmap)).click()
    if (context_hashmap["member_of_rewards"][0] == "Yes"): # we are a rewards member. 
        driver.find_element(By.XPATH, gamble("greet_by_name_or_thank", context_hashmap)).click()
        
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    for i in range(6): # spamming highly satisfied on everything
        driver.find_element(By.XPATH, f"/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[{i + 1}]/td[1]/label").click()
        
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    for i in range(3): # spamming highly satisfied on everything
        driver.find_element(By.XPATH, f"/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[{i + 1}]/td[1]/label").click()
        
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    # we need to check if this order was placed before or after breakfast time. 
    if int(survey_code[3].ljust(4)) >= 1030: # lunchtime order.
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[2]/span/span").click()
        context_hashmap["lunch_order"] = True
    else: # breakfast order.
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/fieldset/div/div/div[1]/span/span").click()
        
    addon_xpath = gamble("additional_order_addons", context_hashmap)
    if addon_xpath != "None":
        driver.find_element(By.XPATH, addon_xpath).click()
        
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    if (context_hashmap["lunch_order"]): # it is a lunch or breakfast
        driver.find_element(By.XPATH, gamble("lunch_menu", context_hashmap)).click()
    else: # breakfast order.
        driver.find_element(By.XPATH, gamble("breakfast_menu", context_hashmap)).click()
        
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    if context_hashmap["additional_order_addons"][0] != "None":
        if context_hashmap["additional_order_addons"][0] == "McCafe":
            driver.find_element(By.XPATH, gamble("mccafe_menu", context_hashmap)).click()
        else: # dessert menu
            driver.find_element(By.XPATH, gamble("dessert_menu", context_hashmap)).click()

        driver.find_element(By.CLASS_NAME, "NextButton").click()
    
        driver.implicitly_wait(0.25)
    
    
    # highly satisfied on food/drink/treats
    if context_hashmap["additional_order_addons"][0] != "None":
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[1]/td[1]/label").click()
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr[2]/td[1]/label").click()
    else:  
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr/td[1]/label").click()
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    
    if context_hashmap["lunch_order"] and context_hashmap["lunch_menu"][0] != "$5 Meal Deal":
        driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/table/tbody/tr/td[2]/label").click()
    
        driver.find_element(By.CLASS_NAME, "NextButton").click()
        
        driver.implicitly_wait(0.25)
    
    driver.find_element(By.XPATH, gamble("reccomend_to_others", context_hashmap)).click()
    driver.find_element(By.XPATH, gamble("return_to_this_mcdonalds", context_hashmap)).click()
    
    driver.find_element(By.CLASS_NAME, "NextButton").click()
    
    driver.implicitly_wait(0.25)
    
    # order-comment part! use chatGPT's API
    if context_hashmap["lunch_order"]:
        order = context_hashmap["lunch_menu"][0]
    else:
        order = context_hashmap["breakfast_menu"][0]
        
    if context_hashmap["additional_order_addons"][0] != "None":
        if context_hashmap["additional_order_addons"][0] == "McCafe":
            order += "and a" + context_hashmap["mccafe_menu"][0]
        else:
            order += "and a" + context_hashmap["dessert_menu"][0]
    mention_highly_satisfied = randrange(1,3) == 1
    if mention_highly_satisfied:
        mention = "highly satisfied"
    else:
        mention = "satisfied (or a synonym to being satisfied)"
    main_prompt = f"You are McDonald's customer who is filling out their Mcdvoice survey online. In around 20-50 words explain how you were {mention} with your visit. Please mention the employee name {employee_name} and how they helped you have an amazing experience, whether that be the speed of service, cleanliness of the restaurant, etc. Here is some additional context: "
    additional_context = f"You ordered via the {context_hashmap["visit_type"]}, An employee did ask if you were using the mobile app (only mention if true) (Y/N): {context_hashmap["asked_about_mobile_app"][0]}, An employee greeted you or thanked you by your name (only mention if this is true) (Y/N): {context_hashmap["greet_by_name_or_thank"][0]}, you ordered a: {order}"
    prompt = main_prompt + additional_context
    response = chat_with_gpt(prompt)
    driver.find_element(By.XPATH, "/html/body/div[1]/main/div[2]/form/div/div[2]/div[2]/div/div/div[2]/textarea").send_keys(response)
    
    """driver.find_element(By.CLASS_NAME, "NextButton").click()
        
    driver.implicitly_wait(0.25)
    
    driver.close()"""
    
    return response

survey_code = "31120-13240-70424-13226-00111-7"
employee_name = "Max"

take_survey(survey_code, employee_name)