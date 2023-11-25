CREATE TABLE viajes (
idS TEXT,
tsO TIMESTAMP,
tsD TIMESTAMP,
price DECIMAL,
tt INT,
dis DECIMAL,
vel DECIMAL,
lonO DECIMAL,
latO DECIMAL,
lonD DECIMAL,
latD DECIMAL
);

COPY viajes
FROM '/docker-entrypoint-initdb.d/rome_u_journeys.csv'
DELIMITER ',' 
CSV HEADER;