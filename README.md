# NARVAL-II Collaboration repository

This repository is intended to facilitate collaboration between NARVAL-II participants.
It will contain metadata, list with resource links and scripts which help to use the measured data in a consistent manner.

Currently, you can find:

* the ``metadata`` folder, containing a growing collection of metadata
* the ``python`` folder, containing the ``narval_ii`` python package with tools to access data and metadata
* the ``docs`` folder, containing the sources for the web page found at https://d70-t.github.io/narval-ii/
* the ``drawings`` folder, containing drawings for common use.

To use the python metadata library, please add the ``python``-folder to your ``PYTHONPATH`` environment variable.
You can now access the metadata using something like:

```python
import narval_ii.metadata
flights = narval_ii.metadata.load_flights()
for flight in flights:
    print(flight.name)
    for segment in flight.segments:
        print(segment.name, segment.start_time, segment.end_time)
        for dropsonde in segment.dropsondes:
            print(dropsonde.date)
```
