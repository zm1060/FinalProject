
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


## FastAPI
Backend framework.

### Celery in Windows
``
 celery -A app.celery_task.tasks worker --loglevel=info -P solo --result-backend=rpc:// -E
``
### Celery in Linux
```
celery -A app.celery_task.tasks worker --concurrency 4 --loglevel=info
```
#### use this to delete all history tasks
``
celery -A app.celery_task.tasks purge -f
``
### Flower
``
flower --app=app.celery_task.tasks --broker=amqp://admin:admin@localhost:5672// --port=5555
``

## Vue
Frontend framework.




### use this to output the dependency
```
pip freeze >requirements.txt
```
