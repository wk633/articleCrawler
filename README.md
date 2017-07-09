# articleCrawler

### virtual environment and project init
```
pip install virtualenv

virtualenv -p python3 articleCrawler

cd articleCrawler
source ./bin/activate

pip install scrapy
scrapy startproject jobboleCrawler

cd jobboleCrawler
scrapy genspider jobbole blog.jobbole.com
scrapy crawl jobbole
```

### related Scrapy knowledge points
- override ItemLoader
- default_output_processor
- MapCompose, TakeFirst, Join
- @classmethod
    - import setting parameters: 
        - https://stackoverflow.com/questions/14075941/how-to-access-scrapy-settings-from-item-pipeline
- twisted async
    - twisted.enterprise.adbapi
        - https://twistedmatrix.com/documents/15.3.0/core/howto/rdbms.html
    -

### Mac OS install mysqlclient error solution
reference: https://github.com/PyMySQL/mysqlclient-python/issues/169#issuecomment-299778504

see tinxin's comment
