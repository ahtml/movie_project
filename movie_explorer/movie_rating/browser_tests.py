import datetime
import os
import time
import unittest

from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from sys import platform

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#   Check the os platform of running computer
if platform == 'linux':
    driver_name = 'chromedriver_linux'
else:
    driver_name = 'chromedriver_mac'

DRIVER_DIR = os.path.join(BASE_DIR, "webdrivers", driver_name)

# If you used different port than 8000, you can change it here.
# But, make sure DO NOT push your change into Git
LOCAL_URL = 'http://127.0.0.1:8000/'
URL = 'http://movieexplorer.ddns.net/'
WAIT_TIME = 3  # wait time for browser to stay open for 3 seconds

# TAG ID
FILTER_BOX_TAG = 'genre'
FILTER_OPTION_TAG = 'option'
SORT_BOX_TAG = 'sort_by'
SORT_OPTION_TAG = 'option'


class ChromeTest(unittest.TestCase):
    # Anything declared in setUp will be executed for all test cases
    def setUp(self):
        # clear database
        self.driver = webdriver.Chrome(DRIVER_DIR)
        # 1. Change to 'LOCAL_URL' instead of 'URL' if you test your local running server.
        # 2. Make sure to run local server before running the TestCases.
        # 3. Finally, Make sure DO NOT push your change here into Git
        self.base_url = LOCAL_URL

    # An individual test case. Must start with 'test_' (as per unittest module)
    def test_home_page(self):
        print("Test home\t")
        self.driver.get(self.base_url)
        # A test to ensure the page has keyword 'The Movie Explorer' in the page title
        self.assertEqual('The Movie Explorer', self.driver.title)

        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results. Make sure to put your image test name.
        self.take_screen_shot('test_homepage')

    # test_ST4_1_is_movie_List_Empty
    def test_st1(self):
        """
        Test for registration. Note, It is the left over from the first sprint, so we do not implement all the test cases
        :return:
        """
        self.driver.get(os.path.join(self.base_url, 'register'))
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Input username
        # Find and select the search box element on the page
        try:
            search_box = self.driver.find_element_by_name('username')
            search_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Email
        try:
            search_box = self.driver.find_element_by_name('email')
            search_box.send_keys('sok@lim.ca')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Password
        try:
            search_box = self.driver.find_element_by_name('password')
            search_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Confirm Password
        try:
            search_box = self.driver.find_element_by_name('confirm_pwd')
            search_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Submit the search box form
        search_box.submit()

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st1')

    def test_st2(self):
        """
        Test for login. Note, It is the left over from the first sprint, so we do not implement  all the test cases
        :return:
        """
        self.driver.get(os.path.join(self.base_url, 'login'))
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Input username
        try:
            search_box = self.driver.find_element_by_name('username')
            search_box.send_keys('sokheng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Password
        try:
            search_box = self.driver.find_element_by_name('password')
            search_box.send_keys('sokheng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Submit the search box form
        search_box.submit()

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st2')

    def test_st4_1(self):
        """
        Display movies for search "Batman Begins"
        There should only be one movie displayed
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("Batman Begins")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        #Press search button
        search_area.submit()

        #Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)
        #
        # # Make sure the results page returned something
        assert "Search Results for: <span id=\"search-result\">Batman Begins</span>" in self.driver.page_source
        try:
            found = self.driver.find_element_by_name('next_page')
        except NoSuchElementException:
            assert True
        try:
            found = self.driver.find_element_by_name('prev_page')
        except NoSuchElementException:
            assert True

        #
        # # Another pause so we can see what's going on
        # time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st4_1')

    def test_st4_2(self):
        """
        Display movies for search "Batman"
        There should be multiple movies displayed
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("Batman")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Press search button
        search_area.submit()

        #Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)

        # Make sure the results page returned something
        assert "Search Results for: <span id=\"search-result\">Batman</span>" in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st4_2')

    def test_st4_3(self):
        """
        Error to check when I blank search is made
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Press search button
        search_area.submit()

        # Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)

        assert "Please enter a movie name in the search bar!" in self.driver.page_source

        # Take a screen shot of the results
        self.take_screen_shot('test_st4_4')

    def test_st4_7(self):
        """
        Check if that non-English characters return movies  # (树)
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("树")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Press search button
        search_area.submit()

        # Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)

        # Make sure the results page returned something
        assert "Search Results for: <span id=\"search-result\">树</span>" in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st4_7')

    def test_st4_8(self):
        """
        Check that the result for the keyword "ekkea" returns string "No results found"
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("ekkea")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Press search button
        search_area.submit()

        # Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)

        # Make sure the results page returned something
        assert "No movies found" in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st4_8')

    def test_st4_9(self):
        """
        Check if the next page and previous page displays movies
        :return: None
        """

        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("Batman")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Press search button
        search_area.submit()

        #Pauses the screen so we have time to confirm we have the right page
        time.sleep(WAIT_TIME)

        # Make sure the results page returned something
        assert "Search Results for: <span id=\"search-result\">Batman</span>" in self.driver.page_source
        assert "Current Page: 1" in self.driver.page_source # make sure the correct page is shown

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Go to next page
        try:
            next_page = self.driver.find_element_by_name('next_page')
            next_page.click()
        except NoSuchElementException:
            raise Exception('Cannot find Element next page')

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        assert "Current Page: 2" in self.driver.page_source # make sure the correct page is shown

        # Go to next page
        try:
            next_page = self.driver.find_element_by_name('prev_page')
            next_page.click()
        except NoSuchElementException:
            raise Exception('Cannot find Element next page')

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        assert "Current Page: 1" in self.driver.page_source  # make sure the correct page is shown

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        self.take_screen_shot('test_st4_9')

    def test_st5_1(self):
        """
        Test to Sort the movies by release date acceding order.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Release Date Ascending':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_1')

    def test_st5_2(self):
        """
        Test to Sort the movies by release date descending order.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Release Date Descending':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_2')

    def test_st5_3(self):
        """
        Test to Sort the movies by Popularity order.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Popularity':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_3')

    def test_st5_4(self):
        """
        Test to Sort the movies by release date ascending order after filtering by genre.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Filter select option
        try:
            filter_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in filter_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Comedy':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')
        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Release Date Ascending':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_4')

    def test_st5_5(self):
        """
        Test to Sort the movies by release date descending order after filtering by genre.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Filter select option
        try:
            filter_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in filter_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Comedy':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')
        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Release Date Descending':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_5')

    def test_st5_6(self):
        """
        Test to Sort the movies by Popularity order after filtering by genre.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm that we arrived at the right page
        time.sleep(WAIT_TIME)

        # Filter select option
        try:
            filter_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in filter_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Comedy':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')
        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Popularity':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st5_6')


    def test_st6_1(self):
        """
        Filtering genre on page 1
        Page number testing needs to be added to the test
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            # TODO the name of genre class may change
            sort_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Action':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)
        self.assertTrue(self.driver.find_element_by_css_selector('[name="next_page"]'))
        # Take a screen shot of the results
        self.take_screen_shot('test_st6_1')

    def test_st6_2(self):
        """
        Filtering genre on page 2
        Page number testing needs to be added to the test
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            # TODO the name of genre class may change
            sort_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Action':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        nextpage = self.driver.find_element_by_css_selector('[name="next_page"]')
        nextpage.click()
        time.sleep(WAIT_TIME)
        self.assertTrue(self.driver.find_element_by_css_selector('[name="prev_page"]'))
        time.sleep(WAIT_TIME)
        # Take a screen shot of the results
        self.take_screen_shot('test_st6_2')


    def test_st6_3(self):
        """
        This testcase is exactly the same as st 5_4
        Test to Sort the movies by release date ascending order after filtering by genre.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Filter select option
        try:
            # TODO the find may change
            filter_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in filter_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Comedy':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')
        # Sort select option
        try:
            # TODO the find may change
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Oldest Release':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st6_3')

    def test_st6_4(self):
        """
        This testcase is exactly the same as st 5_5
        Test to Sort the movies by release date descending order after filtering by genre.
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Filter select option
        try:
            # TODO the find may change
            filter_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in filter_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Comedy':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')
        # Sort select option
        try:
            # TODO the find may change
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Most Recent':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Take a screen shot of the results
        self.take_screen_shot('test_st6_4')

    def test_st7_1and2(self):
        """
        Test login and logout from main page
        Not tested on each page because top banner is independent of page
        :return: None
        """
        self.driver.get(self.base_url)
        # Pauses the screen so we have time to confirm that we arrived at the right page
        time.sleep(WAIT_TIME)

        # Verify login button is there and log in
        try:
            log_in =  self.driver.find_element_by_css_selector("input[type=\"button\"]")
            log_in.click()
        except NoSuchElementException:
            raise  Exception('Cannot find Element Log in')

        # try:
        #     log_in = self.driver.find_element_by_name('log in')
        #     log_in.click()
        # except NoSuchElementException:
        #     raise Exception('Cannot find Element Log in')

        # Using login steps based off of ST2
        # self.driver.get(os.path.join(self.base_url, 'login'))
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Input username
        try:
            search_box = self.driver.find_element_by_name('username')
            search_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Password
        try:
            search_box = self.driver.find_element_by_name('password')
            search_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        # Submit the search box form
        search_box.submit()

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        # Verify logout button is there and logout
        try:
            log_out =  self.driver.find_element_by_css_selector("input[type=\"button\"]")
            log_out.click()
        except NoSuchElementException:
            raise  Exception('Cannot find Element Log out')

        # try:
        #     log_out = self.driver.find_element_by_name('log out')
        #     log_out.click()
        # except NoSuchElementException:
        #     raise Exception('Cannot find Element Log out')

        time.sleep(WAIT_TIME)

        # Verify log in button has reappeared
        try:
            log_in =  self.driver.find_element_by_css_selector("input[type=\"button\"]")
            # log_in.click()
        except NoSuchElementException:
            raise  Exception('Cannot find Element Log in')

        # try:
        #     log_in = self.driver.find_element_by_name('log in')
        # except NoSuchElementException:
        #     raise Exception('Cannot find Element Log in')

        # Take a screen shot of the results
        self.take_screen_shot('test_st7_1and2')


    def test_st8_1(self):
        """
        Test to open movie description from homepage by clicking the movie poster.
        :return: None
        """

        self.driver.get(self.base_url)

        # Pauses the screen so we have time to confirm that we arrived at the right page
        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_poster = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the target movie
        movie_poster.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st8_1') 

    def test_st8_2(self):
        """
        Test to open movie description from search page by clicking the movie image.
        :return: None
        """

        self.driver.get(self.base_url)
        
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        try:
            search_area = self.driver.find_element_by_name('search')
            # search_area.clear()
            search_area.send_keys("Batman Begins")
        except NoSuchElementException:
            raise Exception('Cannot find Element search')

        # Simulate click on the search button
        search_area.submit()

        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the target movie
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st8_2') 


    def test_st8_3(self):
        """
        Test to open movie description after filtering by clicking the movie image.
        :return: None
        """

        self.driver.get(self.base_url)

        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            # TODO the name of genre class may change
            sort_select = self.driver.find_element_by_name(FILTER_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(FILTER_OPTION_TAG):
                if option.text == 'Action':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the search button
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st8_3')


    def test_st8_4(self):
        """
        Test to open movie description after sorting by clicking the movie image.
        :return: None
        """

        self.driver.get(self.base_url)
        
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Sort select option
        try:
            sort_select = self.driver.find_element_by_name(SORT_BOX_TAG)
            for option in sort_select.find_elements_by_tag_name(SORT_OPTION_TAG):
                if option.text == 'Oldest Release':
                    option.click()
                    break
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Make sure the results page returned something
        assert "No results found." not in self.driver.page_source

        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the search button
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st8_4')


    def test_st9_1(self):
        """ 
        Test to rate a movie after log in
        :return: None
        """

        self.driver.get(os.path.join(self.base_url, 'login'))
        
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Input username
        try:
            login_box = self.driver.find_element_by_name('username')
            login_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Password
        try:
            login_box = self.driver.find_element_by_name('password')
            login_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Submit the login form
        login_box.submit()

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        self.driver.get(self.base_url)

        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the search button
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        time.sleep(WAIT_TIME)

        # Find the stars element
        try:
            star = self.driver.find_element_by_css_selector('[for="star-5"]');
        except NoSuchElementException:
            raise Exception('Cannot find Element star')

        # Simulate click on the stars
        star.click()

        time.sleep(WAIT_TIME)

        # Assert that the correct amount of stars are given
        self.assertTrue(self.driver.find_element_by_css_selector('[id="star-5"][checked]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st9_1') 


    def test_st9_2(self):
        """ 
        Test to change the rating of a movie after log in
        :return: None
        """

        self.driver.get(os.path.join(self.base_url, 'login'))
        
        # Pauses the screen so we have time to confirm it arrived at the right page
        time.sleep(WAIT_TIME)

        # Input username
        try:
            login_box = self.driver.find_element_by_name('username')
            login_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Input Password
        try:
            login_box = self.driver.find_element_by_name('password')
            login_box.send_keys('heng')
        except NoSuchElementException:
            raise Exception('Cannot find Element name')

        # Submit the login form
        login_box.submit()

        # Another pause so we can see what's going on
        time.sleep(WAIT_TIME)

        self.driver.get(self.base_url)

        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the search button
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        time.sleep(WAIT_TIME)

        # Find the stars element
        try:
            star = self.driver.find_element_by_css_selector('[for="star-2"]');
        except NoSuchElementException:
            raise Exception('Cannot find Element star')

        # Simulate click on the stars
        star.click()

        time.sleep(WAIT_TIME)

        # Assert that the correct amount of stars are given
        self.assertTrue(self.driver.find_element_by_css_selector('[id="star-2"][checked]'))

        # Take a screen shot of the results
        self.take_screen_shot('test_st9_2')

    def test_st9_3(self):
        """
        Test to make sure there's no stars when you are not logged in
        :return: None
        """
        
        self.driver.get(self.base_url)

        # Pauses the screen so we have time to confirm that we arrived at the right page
        time.sleep(WAIT_TIME)

        # Find the target movie; in this case we open the first movie appeared on the page
        try:
            movie_image = self.driver.find_element_by_name("id_movie")
        except NoSuchElementException:
            raise Exception('Cannot find Element movie_image')

        # Simulate click on the search button
        movie_image.submit()

        time.sleep(WAIT_TIME)

        # Assert that we are in the right page, i.e. description page
        self.assertTrue(self.driver.find_element_by_css_selector('[class="displaying-movie-description"]'))

        # Assert that the stars does not show up
        self.assertTrue(not (self.driver.find_elements_by_css_selector('[class="star"]')))
        
        # Take a screen shot of the results
        self.take_screen_shot('test_st9_3')

    # def test_st10_1(self):
    # 	# print ("starting tc10_1...")
    # 	# print ()
    #     """
    #     Test login and display rated movies history
    #     Not tested on each page because top banner is independent of page
    #     :return: None
    #     """
    #     self.driver.get(self.base_url)
    #     # Pauses the screen so we have time to confirm that we arrived at the right page
    #     time.sleep(WAIT_TIME)
    #
    #     # Verify login button is there and log in
    #     try:
    #         log_in =  self.driver.find_element_by_css_selector("input[type=\"button\"]")
    #         log_in.click()
    #     except NoSuchElementException:
    #         raise  Exception('Cannot find Element Log in')
    #
    #     # try:
    #     #     log_in = self.driver.find_element_by_name('log in')
    #     #     log_in.click()
    #     # except NoSuchElementException:
    #     #     raise Exception('Cannot find Element Log in')
    #
    #     # Using login steps based off of ST2
    #     # self.driver.get(os.path.join(self.base_url, 'login'))
    #     # Pauses the screen so we have time to confirm it arrived at the right page
    #     time.sleep(WAIT_TIME)
    #
    #     # print ("trying to login...")
    #     # print ()
    #     # Input username
    #     try:
    #         search_box = self.driver.find_element_by_name('username')
    #         search_box.send_keys('heng')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Input Password
    #     try:
    #         search_box = self.driver.find_element_by_name('password')
    #         search_box.send_keys('heng')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Make sure the results page returned something
    #     assert "No results found." not in self.driver.page_source
    #
    #     # Submit the search box form
    #     search_box.submit()
    #
    #     # Another pause so we can see what's going on
    #     time.sleep(WAIT_TIME)
    #     # print ("finding My Rating button...")
    #     # print ()
    #     try:
    #         my_movies =  self.driver.find_element_by_css_selector("input[value=\"My Movie Ratings\"]")
    #         my_movies.click()
    #     except NoSuchElementException:
    #         raise  Exception('Cannot find Element My Movies Button')
    #     # print ("finding the movie Logan...")
    #     # print ()
    #     time.sleep(WAIT_TIME)
    #     self.assertTrue(self.driver.find_element_by_css_selector('[class="Logan"]'))
    #     time.sleep(WAIT_TIME)
    #     # print ("finding the the star...")
    #     # print ()
    #     time.sleep(WAIT_TIME)
    #     self.assertTrue(self.driver.find_element_by_css_selector('[src="2_stars.png"]'))
    #     time.sleep(WAIT_TIME)
    #
    #     # print ("movie and stars verified!")
    #     # print ()
    #
    #     self.take_screen_shot('test_st10_1')
    #
    # def test_st10_2(self):
    #
    # 	# print ("starting tc10_2")
    # 	# print ()
    #     """
    #     Test display empty rating history page
    #     Not tested on each page because top banner is independent of page
    #     :return: None
    #     """
    #     # print ("registering a non-rating account...")
    #     # print ()
    #     self.driver.get(os.path.join(self.base_url, 'register'))
    #     # Pauses the screen so we have time to confirm it arrived at the right page
    #     time.sleep(WAIT_TIME)
    #
    #     # Input username
    #     # Find and select the search box element on the page
    #     try:
    #         search_box = self.driver.find_element_by_name('username')
    #         search_box.send_keys('zeeee')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Input Email
    #     try:
    #         search_box = self.driver.find_element_by_name('email')
    #         search_box.send_keys('zeee@yang.ca')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Input Password
    #     try:
    #         search_box = self.driver.find_element_by_name('password')
    #         search_box.send_keys('zeeee')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Input Confirm Password
    #     try:
    #         search_box = self.driver.find_element_by_name('confirm_pwd')
    #         search_box.send_keys('zeeee')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Submit the search box form
    #     search_box.submit()
    #
    #     # Another pause so we can see what's going on
    #     time.sleep(WAIT_TIME)
    #
    #     self.driver.get(self.base_url)
    #     # Pauses the screen so we have time to confirm that we arrived at the right page
    #     time.sleep(WAIT_TIME)
    #
    #     # print ("trying to login...")
    #     # print ()
    #     # Verify login button is there and log in
    #     try:
    #         log_in =  self.driver.find_element_by_css_selector("input[type=\"button\"]")
    #         log_in.click()
    #     except NoSuchElementException:
    #         raise  Exception('Cannot find Element Log in')
    #
    #     # try:
    #     #     log_in = self.driver.find_element_by_name('log in')
    #     #     log_in.click()
    #     # except NoSuchElementException:
    #     #     raise Exception('Cannot find Element Log in')
    #
    #     # Using login steps based off of ST2
    #     # self.driver.get(os.path.join(self.base_url, 'login'))
    #     # Pauses the screen so we have time to confirm it arrived at the right page
    #     time.sleep(WAIT_TIME)
    #
    #     # Input username
    #     try:
    #         search_box = self.driver.find_element_by_name('username')
    #         search_box.send_keys('zeee')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Input Password
    #     try:
    #         search_box = self.driver.find_element_by_name('password')
    #         search_box.send_keys('zeee')
    #     except NoSuchElementException:
    #         raise Exception('Cannot find Element name')
    #
    #     # Make sure the results page returned something
    #     assert "No results found." not in self.driver.page_source
    #
    #     # Submit the search box form
    #     search_box.submit()
    #
    #     # Another pause so we can see what's going on
    #     time.sleep(WAIT_TIME)
    #
    #     # print ("finding My Rating button...")
    #     # print ()
    #     try:
    #         my_movies =  self.driver.find_element_by_css_selector("input[value=\"My Movie Ratings\"]")
    #         my_movies.click()
    #     except NoSuchElementException:
    #         raise  Exception('Cannot find Element My Movies Button')
    #
    #     # print ("no movie rated confirmed!")
    #     # print ()
    #
    #     self.take_screen_shot('test_st10_2')

    def take_screen_shot(self, test_name):
        """
        Taking screen shot of the test result. The purpose is need when the test fail
        :param test_name: Name of screen shot
        :return:
        """
        now = datetime.datetime.now()
        directory = os.path.join(BASE_DIR, 'test_results_img', now.strftime("%Y-%m-%d"))
        if not os.path.exists(directory):
            os.makedirs(directory)
        image_name = '.'.join([test_name + now.strftime("_%H:%M:%S"), 'png'])
        return self.driver.save_screenshot(os.path.join(directory, image_name))

    # Anything declared in tearDown will be executed for all test cases
    def tearDown(self):
        # Close the browser.
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
