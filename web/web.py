import crawl
from multiprocessing import Process

# TRUNCATE links; TRUNCATE urls; TRUNCATE words; INSERT INTO `urls` (`id`, `url`, `hash`, `visited`, `last_visit`, `to_visit`, `domain`, `page_rank`) VALUES (NULL, 'https://www.tudelft.nl/en', 'f92208332f9682f9319e6a53127ce10ed709e8ba91d7dc81e267a0d157d9ee4b', '0', NULL, '0', '', '0');

p1 = Process(target=crawl.launch(1))
p1.start()
p2 = Process(target=crawl.launch(2))
p2.start()
p3 = Process(target=crawl.launch(3))
p3.start()
p4 = Process(target=crawl.launch(4))
p4.start()
p1.join()
p2.join()
p3.join()
p4.join()