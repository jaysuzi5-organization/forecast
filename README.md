# Documentation for forecast
### fastAPI: CRUD operations around an existing table weather_forecast


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/forecast/info         | Basic description of the application and container     |
| GET    | /api/v1/forecast/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/forecast         | List all forecast     | /api/v1/forecast       |
| GET    | /api/v1/forecast/{id}    | Get forecast by ID     | /api/v1/forecast/42    |
| POST   | /api/v1/forecast         | Create new forecast    | /api/v1/forecast       |
| PUT    | /api/v1/forecast/{id}    | Update forecast (full) | /api/v1/forecast/42    |
| PATCH  | /api/v1/forecast/{id}    | Update forecast (partial) | /api/v1/forecast/42 |
| DELETE | /api/v1/forecast/{id}    | Delete forecast        | /api/v1/forecast/42    |


### Access the info endpoint
http://home.dev.com/api/v1/forecast/info

### View test page
http://home.dev.com/forecast/test/forecast.html

### Swagger:
http://home.dev.com/api/v1/forecast/docs