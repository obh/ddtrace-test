This application has a minimal reproducible code to show how ddtrace-run breaks when using `async_to_sync` in some views in django. 

Steps to reproduce:

`python manage.py migrate`
`python manage.py runserver 0.0.0.0:8000`
`curl -k --location 'http://localhost:8000/test-async/'`

This will work since we are not using `ddtrace` as of now. But when I add `ddtrace-run` to the runserver command I get the following exception:

```
Traceback (most recent call last):
  File "/workspaces/crustdata/ddtrace-test/ddtracetest/testapp/views.py", line 20, in test_async_view
    result = async_to_sync(dummy_async_operation)()
  File "/usr/local/lib/python3.8/site-packages/asgiref/sync.py", line 203, in __call__
    loop_future.result()
  File "/usr/local/lib/python3.8/concurrent/futures/_base.py", line 437, in result
    return self.__get_result()
  File "/usr/local/lib/python3.8/concurrent/futures/_base.py", line 389, in __get_result
    raise self._exception
  File "/usr/local/lib/python3.8/concurrent/futures/thread.py", line 57, in run
    result = self.fn(*self.args, **self.kwargs)
  File "/usr/local/lib/python3.8/site-packages/ddtrace/contrib/internal/futures/threading.py", line 36, in _wrap_execution
    return fn(*args, **kwargs)
  File "/usr/local/lib/python3.8/site-packages/asgiref/sync.py", line 241, in _run_event_loop
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
  File "/usr/local/lib/python3.8/asyncio/tasks.py", line 760, in gather
    loop = events.get_event_loop()
  File "/usr/local/lib/python3.8/asyncio/events.py", line 639, in get_event_loop
    raise RuntimeError('There is no current event loop in thread %r.'
RuntimeError: There is no current event loop in thread 'ThreadPoolExecutor-1_0'.
```

Here is the bug: https://github.com/DataDog/dd-trace-py/issues/12556

Separately, I also tried using `import ddtrace.auto`, but that always throws some error when I start the server on some import issue. I haven't tried that in detail. 


