from selenium import webdriver


browser = webdriver.Chrome(executable_path="/Users/tmackan/develop_env/chromedriver")

# browser = webdriver.Chrome()

browser.get('http://localhost:8030')

assert 'Django' in browser.title
