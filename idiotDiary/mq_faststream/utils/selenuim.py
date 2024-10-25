find_by_id: Callable[[str], WebElement] = lambda id_value: webdriver.find_element(By.ID, id_value)
find_by_css: Callable[[str], WebElement] = lambda css_value: webdriver.find_element(By.CSS_SELECTOR, css_value)
