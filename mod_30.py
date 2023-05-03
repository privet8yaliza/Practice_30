import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
	pytest.driver = webdriver.Firefox()
	pytest.driver.get("http://petfriends.skillfactory.ru/login")

	pytest.driver.find_element(By.ID, "email").send_keys("liz@liz8.com")
	pytest.driver.find_element(By.ID, "pass").send_keys("12345")
	pytest.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

	assert pytest.driver.find_element(By.TAG_NAME, "h1").text == "PetFriends"

	pytest.driver.implicitly_wait(10)
	pytest.driver.get("https://petfriends.skillfactory.ru/my_pets")
	pytest.driver.find_element(By.ID, "all_my_pets")
	WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Мои питомцы")))
	WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.LINK_TEXT, "Все питомцы")))
	WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-outline-secondary")))
	WebDriverWait(pytest.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn.btn-outline-success")))
	
	yield

	pytest.driver.quit()


def test_show_my_pets():
	number = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".\\.col-sm-4")))
	# number = pytest.driver.find_element(By.CSS_SELECTOR, ".\\.col-sm-4").text
	elements = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')))
	# elements = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')

	assert len(elements) == int(number.text.split(" ")[1].split("\n")[0])


def test_show_my_pets_photo():
	photo = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//th[@scope="row"]//img[@src=""]')))
	# photo = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//th[@scope="row"]//img[@src=""]')
	elements = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')))
	# elements = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')
	
	assert len(photo) < len(elements) // 2


def test_show_my_pets_without_elements():
	elements_all = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//td')))
	# elements_all = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//td')
	for i in elements_all:
		if i.text == "" or i.text == "None":
			assert False
			

def test_show_my_pets_different_name():
	elements_names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//td[1]')))
	# elements_names = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr//td[1]')

	a = []
	for i in elements_names:
		if i.text not in a:
			a.append(i.text)
		else:
			assert False


def test_show_my_pets_duplicate():
	elements = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')))
	# elements = pytest.driver.find_elements(By.XPATH, '//div[@id="all_my_pets"]//table[@class="table table-hover"]//tbody//tr')
	
	a = []
	for i in elements:
		if i.text not in a:
			a.append(i.text)
		else:
			assert False
