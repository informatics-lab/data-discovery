# data-discovery

## Elasticsearch
Used https://github.com/deviantony/docker-elk to set up local elasticsearch

```python
from elasticsearch import Elasticsearch
import json

client = Elasticsearch()
metadata = json.load(open('./example_nc_headers.json'))

client.index(index='test', doc_type='test', metadata[0])
```

## S3 NetCDF

```bash
conda create --name s3netdf-python2 python=2
conda activate s3netdf-python2
git clone https://github.com/cedadev/S3-netcdf-python
cd S3-netcdf-python
pip install -e ../S3-netcdf-python/
```

```python
from __future__ import print_function
from S3netCDF4._s3netCDF4 import s3Dataset as Dataset
s3_path = "s3://s3/informatics-eupheme/HadGEM3-A-N216/historical/tas/Amon/"
nc_path = "tas_Amon_HadGEM3-A-N216_historical_r1i1p10_200001-200912.nc"

%%time
with Dataset(s3_path + nc_path, mode='r') as s3_data:
    _ = s3_data
```

Simple speed comparison, running this vs. pysssix on laptop. Not a great test but gives an idea of speed:
```
# s3netcdf
CPU times: user 600 ms, sys: 574 ms, total: 1.17 s
Wall time: 9.22 s

# fuse (pysssix) with netcdf4
CPU times: user 8.68 ms, sys: 20.5 ms, total: 29.2 ms
Wall time: 1.8 s

```

Initial thoughts:
- Python 2 and Cython are a bit awkward, curious about reasoning. Possibly compatibility, e.g. with C netcdf library?
- Really two projects in one. Object store for netcdf and also CFAggregate stuff. Direct access to bject store is currently slower than fuse. Until that's optimised we can use CFAggregate over fuse for example.
- They describe decisisons around slicing data on their repo - e.g. 1 variable per file. Looks like we can just use the underlying classes to avoid rewriting original files (https://github.com/cedadev/S3-netcdf-python/blob/master/S3netCDF4/_CFAClasses.pyx). 
- It's early proof of concept code. It's more mature than what we have, and I think we should use it. But if we run into problems we shouldn't be too shy about simply adding the best of theirs to the best of ours.
