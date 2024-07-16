import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def parse_m_and_s_jobs():
    site = 'https://jobs.marksandspencer.com/job-search'

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    max_page = 2  # Количество страниц для парсинга
    result = []

    for page in range(1, max_page + 1):
        if page == 1:
            driver.get(site)
        else:
            driver.get(f'{site}&page={page}')

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'text-2xl.bold.mb-16')))

        job_titles = driver.find_elements(By.CLASS_NAME, 'text-2xl.bold.mb-16')
        job_links = driver.find_elements(By.CLASS_NAME, 'c-btn.c-btn--primary')

        for title, link in zip(job_titles, job_links):
            job_title = title.text
            job_url = link.get_attribute('href')

            result.append({
                'title': job_title,
                'url': job_url
            })

    driver.quit()

    with open('jobs_m_and_s.json', 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4)


if __name__ == '__main__':
    parse_m_and_s_jobs()
