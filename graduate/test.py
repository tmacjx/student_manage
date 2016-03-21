from selenium import webdriver


browser = webdriver.Chrome(executable_path="/Users/tmackan/develop_env/django/lib/python2.7/site-packages/selenium/webdriver/chrome/")
browser.get('http://localhost:8000')

assert 'Django' in browser.title