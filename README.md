
<h1>NLP-based visualizable evaluation information collection and analysis system<br>(基于NLP的可视化评价信息收集与分析系统)
</h1>
<p>By Ming Zuo</p>
<p align="center">

  <a href="https://github.com/zm1060/FinalProject/blob/master/LICENSE">
        <img src="https://img.shields.io/bower/l/bootstrap?style=for-the-badge"
             alt="GitHub license">
  </a>
</p>

<h4 align="center">
    <p>持续维护</p>
</h4>

pypiwin32==223
pywin32==305
## Crawler
This moudle will collect information from websites like JD, weibo...
### modern crawler frameworks.


## NLP
Use NLP framework to analyze information.
### moder nlp solutions


## FastAPI
Backend framework.

### What is FastAPI?
### Why FastAPI?

### Celery in Windows
``
 celery -A app.celery_task.tasks worker --loglevel=info -P solo --result-backend=rpc:// -E
``
#### use this to delete all history tasks
``
celery -A app.celery_task.tasks purge 
``
### Flower
``
flower --app=app.celery_task.tasks --broker=amqp://admin:admin@localhost:5672// --port=5555
``

## Vue
Frontend framework.

### What is Vue?
### Why Vue?
Use Vue Components

## Some ideas
<li>Use scrapydweb or spider-admin-pro to manage various kinds of spiders(crawlers).
<li>And backend provides general processing to the result of spiders. However, for some special sites like weibo, we can provide more features.<br>It means that our frontend must use components. Once we want to support a new website like www.jd.com, we just need to code a new crawler. And use general backend services.




## Development Notes
### use this to output the dependency
```
pip freeze >requirements.txt
```
## How to use?

## How to contribute to my project?