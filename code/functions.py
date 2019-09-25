def graph_pred_vs_actual(actual,pred,data_type):
    plt.scatter(actual,pred,alpha=.3)
    plt.plot(np.linspace(int(min(pred)),int(max(pred)),int(max(pred))),
                 np.linspace(int(min(pred)),int(max(pred)),int(max(pred))))
    plt.title('Actual vs Pred ({} Data)'.format(data_type))
    plt.xlabel('Actual')
    plt.ylabel('Pred')  
    plt.show()
    
def graph_residual(actual,residual,data_type):
    plt.scatter(actual,residual,alpha=.3)
    plt.plot(np.linspace(int(min(actual)),int(max(actual)),int(max(actual))),np.linspace(0,0,int(max(actual))))
    plt.title('Actual vs Residual ({} Data)'.format(data_type))
    plt.xlabel('Actual')
    plt.ylabel('Residual')
    plt.show()

def scrape_weather_url(url):
    # weather data holder to be inserted to pandas dataframe
    high_low, weather_desc, humidity_barometer, wind, date_time = [], [], [], [], []
    
    # open url
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, "lxml")
    days_chain = [x.find_all('a') for x in soup.find_all(class_='weatherLinks')]
    time.sleep(5)
    
    # Load Entire Page by Scrolling to charts
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3.5);") # Scroll down to bottom
    
    # First load of each month takes extra long time. Therefore 'counter' variable is used to run else block first
    counter = 0
    for ix,link in enumerate(days_chain[0]):
        
        '''
        Bottom section tries to solve loading issue by implementing wait feature
        Refer : https://selenium-python.readthedocs.io/waits.html
        '''
        wait = WebDriverWait(driver, 10)
        if counter!=0:
            delay = 3 # seconds
            try:
                myElem = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'weatherLinks')))
            except TimeoutException:
                print("Loading took too much time!" ) 
            day_link = driver.find_element_by_xpath("//div[@class='weatherLinks']/a[{}]".format(ix+1))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='weatherLinks']/a[{}]".format(ix+1))))
            day_link.click()
        else:
            delay = 5 # seconds
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'weatherLinks')))
            except TimeoutException:
                print("Loading took too much time!" ) 
            day_link = driver.find_element_by_xpath("//div[@class='weatherLinks']/a[{}]".format(ix+1))
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='weatherLinks']/a[{}]".format(ix+1))))
            time.sleep(4)
            day_link.click()
            time.sleep(3)
            counter+=1
        
        # Wait a bit for the Javascript to fully load data to be scraped
        time.sleep(2.5)
            
        # Scrape weather data
        high_low.insert(0,driver.find_elements_by_xpath("//div[@class='temp']")[-1].text) #notice elements, s at the end. This returns a list, and I can index it.
        weather_desc.insert(0,driver.find_element_by_xpath("//div[@class='wdesc']").text)
        humidity_barometer.insert(0,driver.find_element_by_xpath("//div[@class='mid__block']").text)
        wind.insert(0,driver.find_element_by_xpath("//div[@class='right__block']").text)
        date_time.insert(0,driver.find_elements_by_xpath("//div[@class='date']")[-1].text)
    return high_low, weather_desc, humidity_barometer, wind, date_time


  

 