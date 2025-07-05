from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from collections import defaultdict
from core import setup_driver, get_model, StudentDetails, TagInfo, TagList, ResponseModel_agent6
from pydantic_ai import Agent

# Initialize driver and model
driver = setup_driver()
model = get_model()

# Define student information
student_info = StudentDetails(
    first_name="Rohan",
    middle_name="Sadanand",
    last_name="Disa",
    phone_number="213-245-6745",
    address="Earth",
    citizenship="India",
    sex="Male",
    gender="Male",
    email="rohandisa2002@gmail.com",
    confirmed_email="rohandisa2002@gmail.com",
    password="Rinkudisa#15",
    zipcode="411021",
    city="Pune",
    street="Behind Maratha Mandir",
    birth_month="10",
    birth_day="15",
    birth_year="2002",
    degree="Bachelor of Technology",
    ethnicity="Asian",
    undergrad_college="Maharashtra Institute of Technology World Peace University"
)

url = "https://www.applyweb.com/forms/worcestg"
driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "input")))

# Collect input elements
input_elements = driver.find_elements(By.XPATH, '//form//input')
select_elements = driver.find_elements(By.XPATH, '//form//select')
text_details = []
for elem in input_elements:
    text_details.append({
        'tag': 'input',
        'type': elem.get_attribute('type'),
        'name': elem.get_attribute('name'),
        'id': elem.get_attribute('id'),
        'text': elem.text.strip()
    })

for elem in select_elements:
    field_info = {
        'tag': 'select',
        'type': 'select-one',
        'name': elem.get_attribute('name'),
        'id': elem.get_attribute('id'),
        'text': ''
    }
    try:
        select = Select(elem)
        options = select.options
        field_info['text'] = [opt.text.strip() for opt in options if opt.text.strip()]
    except: pass
    text_details.append(field_info)

# Chunk fields and feed to LLM
MAX_FORM_ITEMS = 10
chunks = [text_details[i:i + MAX_FORM_ITEMS] for i in range(0, len(text_details), MAX_FORM_ITEMS)]

all_inputs = []
for chunk in chunks:
    agent = Agent(
        model=model,
        result_type=TagList,
        retries=3,
        system_prompt=(
            f"""
            You are a form-filling assistant.

            You are given:

            chunk: a list of form input elements, each with metadata like name, type, id, and available options.

            student_info: a structured object based on the StudentDetails model, containing values for fields like name, email, birthdate, etc.

            Your task is to:

            Extract the name (or id, if name is missing) from each input in {chunk}.

            Look up the corresponding value from {student_info} using that name.

            Match this value to the input element appropriately depending on its type
            """
        )
    )
    response = agent.run_sync("Follow the prompt")
    all_inputs.append(response.data)

# Fill the form fields
for data_group in all_inputs:
    for field_group in data_group:
        for field_info in field_group:
            try:
                if field_info.type == "radio":
                    xpath = f"//input[@type='radio'][@name='{field_info.name}'][@value='{field_info.value}']"
                    radio_element = driver.find_element(By.XPATH, xpath)
                    if not radio_element.is_selected():
                        driver.execute_script("arguments[0].click();", radio_element)

                elif field_info.type == "select":
                    select_elem = Select(driver.find_element(By.NAME, field_info.name))
                    matched = False
                    for option in select_elem.options:
                        if option.get_attribute("value").lower() == field_info.value.lower():
                            select_elem.select_by_value(option.get_attribute("value"))
                            matched = True
                            break
                    if not matched:
                        select_elem.select_by_visible_text(field_info.value)

                else:
                    element = driver.find_element(By.NAME, field_info.name)
                    if element.get_attribute("value").strip(): continue
                    element.clear()
                    element.send_keys(field_info.value)

            except Exception as e:
                print(f"Error filling field '{field_info.name}': {e}")

# Decide which button to click
button_elements = driver.find_elements(By.XPATH, '//form//button')
buttons = []
seen_buttons = set()
for button in button_elements:
    name = button.get_attribute('name')
    if name and name not in seen_buttons:
        buttons.append({"tag": "button", "name": name, "text": button.text.strip()})

agent_nav = Agent(
    model=model,
    result_type = TagList,
    retries=3,
    system_prompt=(f"""
                    You are a form-filling assistant for a university webpage. Your task is to choose the most appropriate button or link to interact with next in the form-filling process.

                    You are given:

                    - {buttons}: a list of all currently visible, clickable button elements  

                    Only select from the provided buttons and links. Do NOT invent or guess elements that aren't in the list.

                    ---

                    Follow this decision logic strictly:

                    1. If a button or link performs a required validation step (e.g., "Search for College", "Verify Email", "Check Zip Code"), and it hasn't already been handled, select it first.

                    2. **If optional buttons like "Add Another Institution", "Edit Address", or "Add Phone Number" are present**, consider them — but **only select them if the user actually needs to add or change something.**  
                    (For example, if the user has attended only one institution, skip "Add Another Institution.")

                    3. **If all required and optional data is complete**, select a button or link that clearly **advances the form**, such as:
                    "Next", "Continue", "Submit", "Confirm", or "Next Page".

                    ---

                    Do not re-select buttons that have already been clicked.  
                    Do not invent new buttons or links.  
                    Return only the exact visible text of the selected button or link.
                """)
)
response = agent_nav.run_sync("Follow the prompt")

if response.data.type == "button":
    try:
        button = driver.find_element(By.XPATH, f"//button[normalize-space(text())='{response.data.value}']")
        name = button.get_attribute('name')
        if name not in seen_buttons:
            seen_buttons.add(name)
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            driver.execute_script("arguments[0].click();", button)
    except NoSuchElementException:
        print("Button not found.")
