import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(autouse=True)
def testing():
    pytest.driver = webdriver.Chrome('C:/Chromedriver/chromedriver.exe')
    pytest.driver.get('http://petfriends.skillfactory.ru/login')

    pytest.driver.implicitly_wait(5)

    yield

    pytest.driver.quit()

# У всех питомцев есть имя, возраст, порода
def test_all_my_pets_have_name_age_breed():
    pytest.driver.find_element(By.ID, 'email').send_keys('clairessse@bk.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('petfriends')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, u'Мои питомцы').click()

    names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')))
    breed = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[2]')))
    age = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[3]')))

    for i in range(len(names)):
        assert names[i].text != ''
        assert breed[i].text != ''
        assert age[i].text != ''

# На странице есть все питомцы
def test_page_contains_all_my_pets():
    pytest.driver.find_element(By.ID, 'email').send_keys('clairessse@bk.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('petfriends')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, u'Мои питомцы').click()

    user_statistics = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'.col-sm-4 left')]")))
    my_pets_qty = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))

    print(user_statistics.text.split("\n")[1].split(': ')[1])
    print(len(my_pets_qty))

    assert str(len(my_pets_qty)) == user_statistics.text.split("\n")[1].split(': ')[1]

# У всех питомцев разные имена
def test_all_my_pets_have_dif_names():
    pytest.driver.find_element(By.ID, 'email').send_keys('clairessse@bk.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('petfriends')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, u'Мои питомцы').click()

    names = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/td[1]')))

    list_names = [names[i].text for i in range(len(names))]
    set_names = set(list_names)

    print(list_names)
    print(set_names)

    assert len(list_names) == len(set_names)

# Хотя бы у половины питомцев есть фото
def test_half_my_pets_have_photo():
    pytest.driver.find_element(By.ID, 'email').send_keys('clairessse@bk.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('petfriends')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, u'Мои питомцы').click()

    user_statistics = WebDriverWait(pytest.driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class,'.col-sm-4 left')]")))
    images = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr/th/img')))

    pets_with_photo = []
    for i in range(len(images)):
        if images[i].get_attribute('src') != "":
            pets_with_photo.append(i)

    pets_qty = int(user_statistics.text.split("\n")[1].split(': ')[1])

    print(pets_qty // 2)
    print(len(pets_with_photo))

    assert pets_qty // 2 <= len(pets_with_photo)

# В списке нет повторяющихся питомцев
def test_all_my_pets_unique():
    pytest.driver.find_element(By.ID, 'email').send_keys('clairessse@bk.ru')
    pytest.driver.find_element(By.ID, 'pass').send_keys('petfriends')
    pytest.driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
    pytest.driver.find_element(By.LINK_TEXT, u'Мои питомцы').click()

    my_pets_qty = WebDriverWait(pytest.driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="all_my_pets"]/table/tbody/tr')))

    list_pets = [my_pets_qty[i].text.replace(' ', '').lower() for i in range(len(my_pets_qty))]
    set_pets = set(list_pets)

    print(list_pets)
    print(set_pets)

    assert len(list_pets) == len(set_pets)
