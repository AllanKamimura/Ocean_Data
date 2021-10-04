# Ocean Data
----
2021 Nasa Space Apps Challenge


## How to use the API
`git clone https://github.com/AllanKamimura/Ocean_Data.git`

`pip install requirements`

### Start the server
`uvicorn main:app --reload`

### Request Example
params:
1.  latitude [-90:90]

2.  longitude [-180:180]

3.  date [YYYY-MM-DD]
#### Map
`http://127.0.0.1:8000/map/?lat=-23.96083&lon=-46.33361&date=2021-10-08`

#### Data JSON
`http://127.0.0.1:8000/data/?lat=-23.96083&lon=-46.33361&date=2021-10-08`

## How to train the model
https://colab.research.google.com/github/AllanKamimura/Ocean_Data/blob/main/model_train.ipynb
