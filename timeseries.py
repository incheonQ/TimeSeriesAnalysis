from collections.abc import Sequence

def moving_average_methods(
    data: Sequence[float], window_size: int
)->list[float | None]:
    
    if window_size < 1:
        raise ValueError
        
    if window_size > len(data):
        raise ValueError

    levels: list[float | None] = []
    
    for i in range(len(data)):
        if i < window_size - 1:
            levels.append(None)
        else:
            window = data[i-window_size+1 : i+1]
            level_value = sum(window)/window_size
            levels.append(level_value)
    return levels

def exponential_smoothing_methods(
    data: Sequence[float], alpha: float = None
)-> list[float]:

    if alpha == None:
        alpha = 2 / ( 1 + len(data))
        print(f"Set alpha: {alpha}")

    levels = []
    
    first_level = sum(data)/len(data)
    levels.append(first_level)
    
    for i in range(len(data)):
        level_value = alpha * data[i] + ( 1 - alpha ) * levels[i]
        levels.append(level_value)

    return levels

def betas(data):
    Xbar = sum(range(len(data)+1))/len(data)
    Ybar = sum(data)/len(data)

    X_minus_Xbar = [x - Xbar for x in range(1, len(data)+1)]
    Y_minus_Ybar = [y - Ybar for y in data]

    X_minus_Xbar_square = [x**2 for x in X_minus_Xbar]
    X_minus_Xbar_times_y_minus_Ybar = [x*y for x, y in zip(X_minus_Xbar, Y_minus_Ybar)]

    b1 = sum(X_minus_Xbar_times_y_minus_Ybar)/ sum(X_minus_Xbar_square)

    b0 = Ybar - b1 * Xbar
    return b0, b1

def holt_model(
    data: Sequence[float], 
    alpha: float, 
    beta: float, 
)->list[float]:

    level0, trend0 = betas(data)
    forecast0 = level0 + trend0
    
    levels = []
    trends = []
    forecasts = []

    levels.append(level0)
    trends.append(trend0)
    forecasts.append(forecast0)

    for i in range(len(data)):
        level_value = alpha*data[i] + (1-alpha)*(levels[i]+trends[i])
        levels.append(level_value)
        trend_value = beta*(levels[i+1]-levels[i])+(1-beta)*trends[i]
        trends.append(trend_value)
        forecast_value = level_value + trend_value
        forecasts.append(forecast_value)

    return forecasts

def winters_model(
    data: Sequence[float],
    P: int,
    alpha: float, 
    beta: float, 
    gamma: float
)->list[float]:
    
    level0, trend0 = betas(data)

    # raise ValueError needs here
    r = len(data)//P

    # Preparation to calculate initial seasonal indexs
    seasonal_indexs = []
    for i in range(r):
        blocks = needs[i*P:i*P+P]
        for j in blocks:
            seasonal_index = j / (sum(blocks)/len(blocks))
            seasonal_indexs.append(seasonal_index)

    # Calculate initial seasonal indexs 1 ~ P
    for i in range(P):
        initial_seasonal_index = sum(seasonal_indexs[i::4])/3
        seasonal_indexs[i] = initial_seasonal_index
    
    # Calculate levels and Trends
    levels = []
    levels.append(level0)
    trends = []
    trends.append(trend0)

    for i in range(len(data)):
        level_value = alpha*(data[i]/seasonal_indexs[i])+(1-alpha)*(levels[i]+trends[i])
        levels.append(level_value)
        
        trend_value = beta*(levels[i+1]-levels[i])+(1-beta)*trends[i]
        trends.append(trend_value)

    # Calculate Seasonal Indexs
    seasonals = seasonal_indexs[:P]

    for i in range(len(data)-P):
        seasonal_value = gamma*(data[i]/levels[i+1])+(1-gamma)*seasonals[i]
        seasonals.append(seasonal_value)

    print(seasonals)

    # Predict
    forecasts = []

    for i in range(len(data)):
        forecast_value = (levels[i]+trends[i])*seasonals[i]
        forecasts.append(forecast_value)

    return forecasts
        
    

    
    
