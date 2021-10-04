import numpy as np
import pandas as pd
import tensorflow as tf
import plotly.express as px
import plotly.graph_objects as go

from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")

def load_model():
	model = tf.keras.models.load_model("./model/notlstm2.h5")
	return model
model = load_model()

def draw_map(lat, lon, date):
	month = int(date[5:7])
	test_lat = np.array([lat]) / 90
	test_lon = np.array([lon + 180]) / 360
	test_month = np.array([month]) / 12
	pred_lat = [lat / 90]
	pred_lon = [(lon + 180) / 360]

	for i in range(10):
		prev_lat, prev_lon = model([np.expand_dims(test_lat, axis = 0), 
									np.expand_dims(test_lon, axis = 0),
									np.expand_dims(test_month, axis = 0)])

		prev_lat = prev_lat.numpy().squeeze()
		prev_lon = prev_lon.numpy().squeeze()

		pred_lat.append(prev_lat)
		pred_lon.append(prev_lon)

		test_lat = prev_lat
		test_lon = prev_lon

	test_df = {"lat": np.array(pred_lat) * 90,
			   "lon": np.array(pred_lon) * 360 - 180,
			   "size": np.arange(10),
			   "name": ["{}".format(month) for month in np.arange(10)]}

	fig = go.Figure(layout = dict(height = 600, width = 800))

	fig.add_trace(go.Scattergeo(
		lat = test_df["lat"],
		lon = test_df["lon"],
		text = test_df["name"],
		mode = 'lines+markers+text',
		marker = dict(
			color = "rgb(0, 204, 150)",
			size = test_df["size"] + 20,
			cmin = 0,
			cmax= 16,
			)
		))

	fig.update_layout(
		geo = dict(
			lataxis = dict(
				range = [test_df["lat"].min() - 20, test_df["lat"].max() + 20],
				showgrid = True,
				dtick = 10
			),
			lonaxis = dict(
				range = [test_df["lon"].min() - 40, test_df["lon"].max() + 40],
				showgrid = True,
				dtick = 20
			)
		)
	)
	
	fig_path = "./map/fig1.png"
	fig.write_image(fig_path)
	fig.show()
	return fig_path
	
@app.get("/")
def read_root():
	return {"Hello": "World"}

@app.get("/items2/")
async def read_item(lat: float, lon: float):
	return lat, lon

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
	return {"item_id": item_id, "q": q}

@app.get("/map/", response_class=HTMLResponse)
async def read_item(request: Request, lat: float, lon: float, date: str):
	draw_map(lat, lon, date)
	return templates.TemplateResponse("item.html", {"request": request, 
													"lat": lat,
													"lon": lon,
													"date": date})