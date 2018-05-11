SELECT date_trunc('hour', a.datetime) as datetime,
ROUND(AVG((a.condition -> 'current_observation' ->> 'temp_f')::numeric), 1) AS outside,
ROUND(AVG((b.temp)::numeric), 1) AS inside
FROM arlington_weather_condition as a, inside_temp as b
WHERE date_trunc('hour', a.datetime) = date_trunc('hour', b.datetime)
GROUP BY date_trunc('hour', a.datetime)
ORDER BY date_trunc('hour', a.datetime)
