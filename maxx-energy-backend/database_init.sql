
DROP TABLE IF EXISTS energy_data;

CREATE TABLE IF NOT EXISTS energy_data (
    id SERIAL PRIMARY KEY,
    plant_name VARCHAR(100),
    location VARCHAR(100),
    energy_generated_kWh FLOAT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO energy_data (plant_name, location, energy_generated_kWh, timestamp)
VALUES
('Solar Plant A', 'California', 12345.67, '2025-02-10 08:30:00'),
('Solar Plant B', 'Nevada', 9876.54, '2025-02-10 09:00:00'),
('Solar Plant C', 'Arizona', 5678.90, '2025-02-10 09:30:00'),
('Solar Plant D', 'Texas', 15678.32, '2025-02-10 10:00:00'),
('Solar Plant E', 'Florida', 11234.56, '2025-02-10 10:30:00'),
('Solar Plant F', 'New Mexico', 13578.44, '2025-02-10 11:00:00'),
('Solar Plant G', 'Utah', 14233.89, '2025-02-10 11:30:00'),
('Solar Plant H', 'Colorado', 12098.78, '2025-02-10 12:00:00'),
('Solar Plant I', 'Oregon', 11345.23, '2025-02-10 12:30:00'),
('Solar Plant J', 'Washington', 10987.65, '2025-02-10 13:00:00'),
('Solar Plant K', 'Idaho', 12300.45, '2025-02-10 13:30:00'),
('Solar Plant L', 'Montana', 15000.12, '2025-02-10 14:00:00'),
('Solar Plant M', 'Wyoming', 9800.76, '2025-02-10 14:30:00'),
('Solar Plant N', 'North Dakota', 8700.50, '2025-02-10 15:00:00'),
('Solar Plant O', 'South Dakota', 7600.35, '2025-02-10 15:30:00'),
('Solar Plant P', 'Kansas', 8800.67, '2025-02-10 16:00:00'),
('Solar Plant Q', 'Nebraska', 9300.45, '2025-02-10 16:30:00'),
('Solar Plant R', 'Oklahoma', 11100.89, '2025-02-10 17:00:00'),
('Solar Plant S', 'Arkansas', 10500.22, '2025-02-10 17:30:00'),
('Solar Plant T', 'Louisiana', 11700.33, '2025-02-10 18:00:00');
