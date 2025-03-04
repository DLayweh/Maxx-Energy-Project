
-- Create the table if it doesn't exist
CREATE TABLE IF NOT EXISTS energy_data (
    id SERIAL PRIMARY KEY,
    plant_name VARCHAR(100),
    location VARCHAR(100),
    energy_generated_kWh DECIMAL(10,2),
    temperature_celsius DECIMAL(5,2),
    solar_radiation_Wm2 DECIMAL(6,2),
    panel_efficiency DECIMAL(4,2),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO energy_data (plant_name, location, energy_generated_kWh, temperature_celsius, solar_radiation_Wm2, panel_efficiency, timestamp) VALUES
('Desert Sun Solar', 'California', 15432.78, 28.4, 820.5, 18.7, '2025-03-01 08:00:00'),
('Silver Peak Solar', 'Nevada', 13987.56, 30.1, 780.3, 17.9, '2025-03-01 09:00:00'),
('Phoenix Solar Farm', 'Arizona', 18234.45, 32.8, 850.2, 19.2, '2025-03-01 10:00:00'),
('Lone Star Solar', 'Texas', 14678.22, 31.5, 795.8, 18.4, '2025-03-01 11:00:00'),
('Sunshine State Solar', 'Florida', 12980.34, 29.2, 770.4, 17.5, '2025-03-01 12:00:00'),
('Rio Grande Solar', 'New Mexico', 17450.89, 33.0, 830.7, 19.0, '2025-03-01 13:00:00'),
('Great Basin Solar', 'Utah', 13600.12, 27.8, 760.2, 16.9, '2025-03-01 14:00:00'),
('Rocky Mountain Solar', 'Colorado', 19870.56, 26.5, 890.1, 20.3, '2025-03-01 15:00:00'),
('Portland Solar Fields', 'Oregon', 11234.78, 22.3, 670.5, 15.8, '2025-03-01 16:00:00'),
('Cascade Solar', 'Washington', 10890.45, 21.7, 650.2, 15.4, '2025-03-01 17:00:00'),
('Peach State Solar', 'Georgia', 13567.34, 28.0, 740.3, 17.3, '2025-03-01 18:00:00'),
('Palmetto Solar Farm', 'South Carolina', 14278.56, 29.4, 765.7, 17.8, '2025-03-01 19:00:00'),
('Blue Ridge Solar', 'North Carolina', 15745.78, 30.8, 800.2, 18.6, '2025-03-01 20:00:00'),
('Heartland Solar Plant', 'Kansas', 16890.45, 32.2, 820.9, 19.1, '2025-03-01 21:00:00'),
('Delta Solar Fields', 'Mississippi', 12123.67, 29.9, 710.6, 16.5, '2025-03-01 22:00:00'),
('Bayou Solar Farm', 'Louisiana', 15978.34, 31.3, 780.1, 18.3, '2025-03-01 23:00:00'),
('Coal Country Solar', 'West Virginia', 12765.98, 24.5, 690.3, 16.0, '2025-03-02 00:00:00'),
('Appalachian Solar', 'Tennessee', 13890.23, 27.2, 720.5, 17.1, '2025-03-02 01:00:00'),
('Midwest Solar Hub', 'Illinois', 14123.76, 25.8, 730.8, 17.4, '2025-03-02 02:00:00'),
('Prairie Sun Solar', 'Nebraska', 15078.12, 28.7, 780.5, 18.0, '2025-03-02 03:00:00'),
('Windy Plains Solar', 'Oklahoma', 13298.45, 29.5, 750.2, 17.2, '2025-03-02 04:00:00'),
('Badlands Solar', 'South Dakota', 11900.89, 26.3, 690.4, 16.3, '2025-03-02 05:00:00'),
('Bison Ridge Solar', 'North Dakota', 11345.78, 24.0, 670.1, 15.7, '2025-03-02 06:00:00'),
('Keystone Solar Fields', 'Pennsylvania', 13045.23, 27.1, 710.3, 16.8, '2025-03-02 07:00:00'),
('Empire State Solar', 'New York', 12879.56, 23.4, 695.6, 16.2, '2025-03-02 08:00:00');
