"""
Define the `RedditScraper` class that stores attributes to define a subreddit name and date range.
Included methods use these attributes to scrape either comments or posts in given subreddit within date range.
The result of the above is to return a pandas data frame of results and save to desired location,
using the method as_data_frame(self, 'comments') or as_data_frame(self, 'posts'). Other methods can save
the data frame directly from the scraped results, and of course conduct scraping.

This script does not create any instances, rather just defines the class itself!
"""

# Modules needed to create instances of the class defined in this script:
#import os
#import pandas as pd
#import praw
#from psaw import PushshiftAPI
#import datetime as dt
#from datetime import datetime
#from time import sleep

class RedditScrape:
  def __init__(self, subreddit_name, start_epoch, end_epoch):
    """
    :type subreddit_name: str
    :type start_epoch: datetime
    :type end_epoch: datetime
    """
    import pandas as pd
    from psaw import PushshiftAPI # usually has to be installed on Colab
    # Define attributes (also called instance variables)
    self.api = PushshiftAPI()
    self.subreddit_name = subreddit_name
    self.start_epoch = start_epoch
    self.end_epoch = end_epoch
    self.default_filter = ['author', 'created_utc', 'id', 'is_video', 'num_comments',
                          'pinned', 'post_hint', 'retrieved_on', 'score',
                          'subreddit', 'subreddit_subscribers', 'thumbnail',
                          'thumbnail_height', 'thumbnail_width', 'url']

  
  # Here's the method to scrape comments, specifically using pushshift api
  def scrape_comments(self, filter = None):
    """
    Scrape comments, create self.comments attribute
    """
    import pandas as pd
    if filter is None:
      filter_ = self.default_filter
    else:
      filter_ = filter
    result = self.api.search_comments(subreddit=self.subreddit_name,
                                 filter=filter_,
                                 after = self.start_epoch, 
                                 before = self.end_epoch)
    self.comments = pd.DataFrame([x.d_ for x in result]) 
    
  def scrape_posts(self, filter = None):
    """
    Scrape submissions, calling them `posts` for short, that are posted to boards directly
    """
    import pandas as pd
    if filter is None:
      filter_ = self.default_filter
    else:
      filter_ = filter
    result = self.api.search_submissions(subreddit=self.subreddit_name,
                                 filter = filter_,
                                 after = self.start_epoch, 
                                 before = self.end_epoch)
    self.posts = pd.DataFrame([x.d_ for x in result]) # extract into list, save as attribute
  
  # A method to save the desired data (comments, or submissions/posts)
  # The purpose of this method is simply to facilitate saving with the proper encoding
  def save(self, attribute_name, filename):
    """
    :type attribute_name: str
    :type filename: str
    """
    import pandas
    x = getattr(self, attribute_name)
    x.to_csv(filename, encoding='utf-8-sig', index = False)
