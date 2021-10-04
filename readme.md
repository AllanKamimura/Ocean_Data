# Ocean Data
----
2021 Nasa Space Apps Challenge


## How to use the API
`git clone https://github.com/AllanKamimura/Ocean_Data.git`

`pip install requirements`

### Start the server
`uvicorn main:app --reload`

### Request Example
`http://127.0.0.1:8000/map/?lat=-23.96083&lon=-46.33361&date=2021-10-08`

latitude [-90:90]

longitude [-180:180]

data [YYYY-MM-DD]