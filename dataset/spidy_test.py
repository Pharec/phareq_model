from spidy import crawler

"""
 Global options to check (what is the default and what to change)
    1- Tread count
    2- Start (url seed list)
    3- HEADER
    ...
"""

# crawler.RESTRICT = True
crawler.THREAD_COUNT = 1
crawler.START = ['https://splonline.com.sa']
crawler.HEADER = crawler.HEADERS['Firefox']
crawler.SAVE_PAGES = False
crawler.SAVE_WORDS = False
crawler.SAVE_COUNT = 10
crawler.MAX_NEW_ERRORS = 10
crawler.MAX_KNOWN_ERRORS = 10
crawler.MAX_HTTP_ERRORS = 10
crawler.MAX_NEW_MIMES = 10
crawler.TODO_FILE = 'crawler_todo.txt'
crawler.DONE_FILE = 'crawler_done.txt'
crawler.WORD_FILE = 'crawler_words.txt'

for start in crawler.START:
    crawler.TODO.put(start)
crawler.DONE = crawler.queue.Queue()

robots_index = crawler.RobotsIndex(
    crawler.RESPECT_ROBOTS,
    crawler.HEADER['User-Agent']
)

# Spawn threads here
crawler.spawn_threads(robots_index)
