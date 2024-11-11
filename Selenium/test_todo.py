from Selenium.base import BaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

class TestAddTodoItem(BaseTest):

    def test_add_todo_item(self):
        self.login()  
        
        add_todo_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Add Todo')]")
        add_todo_button.click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]"))
        )

        rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]")
        last_row = rows[-1]

        input_fields = last_row.find_elements(By.XPATH, ".//input")
        save_button = last_row.find_elements(By.XPATH, ".//button")[0]

        if len(input_fields) >= 2:
            title_input = input_fields[0]
            description_input = input_fields[1]

            title_input.send_keys('Test TODO Title')
            description_input.send_keys('Test TODO Description')

            save_button.click()

            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'Added new todo')]"), 'Added new todo')
            )
            time.sleep(2)
        else:
            raise Exception("Couldn't find both title and description input fields.")

        print("Add Test Case Passed")


    def test_edit_todo_item(self):

        
        rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]")
        last_row = rows[-1]  # Get the last row

        # Assuming the title and description inputs are in the last row
        # Find all input fields in the last row and interact with them
        edit_button = last_row.find_elements(By.XPATH, ".//button")[0]

        edit_button.click()

        input_fields = last_row.find_elements(By.XPATH, ".//input")

        # If there are two input fields, assume the first is for the title and the second for the description
        if len(input_fields) >= 2:
            title_input = input_fields[0]
            description_input = input_fields[1]

            title_input.send_keys('\ue003' * len(title_input.get_attribute('value')))
            description_input.send_keys('\ue003' * len(description_input.get_attribute('value')))

            title_input.send_keys('Updated TODO Title')
            description_input.send_keys('Updated TODO Description')

        else:
            print("Error: Couldn't find both title and description input fields.")

        # Save the TODO
        edit_button.click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'Todo has been updated')]"), 'Todo has been updated')
            )
        time.sleep(2)


        print("Edit Test Case Passed")

    def test_delete_todo_item(self):
        
        
        rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]")
        last_row = rows[-1]  # Get the last row

        # Assuming the title and description inputs are in the last row
        # Find all input fields in the last row and interact with them
        delete_button = last_row.find_elements(By.XPATH, ".//button")[1]

        delete_button.click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'Todo has been deleted')]"), 'Todo has been deleted')
            )

        time.sleep(2)


        print("Delete Test Case Passed")

    
    def test_add_incorrect_todo_item(self):
        
        add_todo_button = self.driver.find_element(By.XPATH, "//button[contains(., 'Add Todo')]")
        add_todo_button.click()

        WebDriverWait(self.driver, self.TIMEOUT).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]"))
        )

        rows = self.driver.find_elements(By.XPATH, "//div[contains(@class, 'MuiDataGrid-row')]")
        last_row = rows[-1]

        input_fields = last_row.find_elements(By.XPATH, ".//input")
        save_button = last_row.find_elements(By.XPATH, ".//button")[0]

        if len(input_fields) >= 2:
            title_input = input_fields[0]
            description_input = input_fields[1]

            title_input.send_keys('')
            description_input.send_keys('')

            save_button.click()

            WebDriverWait(self.driver, self.TIMEOUT).until(
                EC.text_to_be_present_in_element((By.XPATH, "//*[contains(text(), 'Failed to add todo')]"), 'Failed to add todo')
            )
            time.sleep(2)
        else:
            raise Exception("Couldn't find both title and description input fields.")

        print("Failed Todo Test Case Passed")