CREATE DATABASE fitness_logs;
USE fitness_logs;

CREATE TABLE workouts(
    id INT PRIMARY KEY AUTO_INCREMENT,
    exercise VARCHAR(255) NOT NULL,
    sets INT NOT NULL,
    reps INT NOT NULL,
    weights DECIMAL(5,2),
    workout_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);
