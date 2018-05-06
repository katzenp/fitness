 -- Personal Data --------------------------------------------------------------
CREATE TABLE IF NOT EXISTS person
(
    person_id SMALLINT UNSIGNED AUTO_INCREMENT,
    registration_date DATE NOT NULL;
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender ENUM('M','F') NOT NULL,
    birth_date DATE NOT NULL,
    street VARCHAR(20),
    city VARCHAR(100),
    state VARCHAR(20),
    country VARCHAR(20),
    postal_code VARCHAR(50),
    email VARCHAR(50),
    CONSTRAINT pk_person PRIMARY KEY (person_id)
);


CREATE TABLE IF NOT EXISTS goals
(
    goal_id SMALLINT UNSIGNED AUTO_INCREMENT,
    person_id SMALLINT UNSIGNED,
    entry_date DATE NOT NULL,
    fitness ENUM('maintain', 'improve'),
    nutrition ENUM('cut', 'maintain', 'bulk'),
    CONSTRAINT pk_goal_id PRIMARY KEY (goal_id),
    CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES person (person_id)
);


CREATE TABLE IF NOT EXISTS body_weight
(
    record_id SMALLINT UNSIGNED AUTO_INCREMENT,
    person_id SMALLINT UNSIGNED,
    entry_date DATE NOT NULL,
    height FLOAT,
    weight FLOAT NOT NULL,
    body_fat FLOAT
    CONSTRAINT pk_record_id PRIMARY KEY (record_id),
    CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES person (person_id)
);


CREATE TABLE IF NOT EXISTS body_measurement
(
    record_id SMALLINT UNSIGNED AUTO_INCREMENT,
    person_id SMALLINT UNSIGNED,
    entry_date DATE NOT NULL,
    l_wrist FLOAT,
    l_forearm FLOAT,
    l_arm FLOAT,
    l_ankle FLOAT,
    l_calf FLOAT,
    l_thigh FLOAT,
    r_forearm FLOAT,
    r_wrist FLOAT,
    r_arm FLOAT,
    r_ankle FLOAT,
    r_calf FLOAT,
    r_thigh FLOAT,
    waist FLOAT,
    chest FLOAT,
    neck FLOAT,
    CONSTRAINT pk_record_id PRIMARY KEY (record_id),
    CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES person (person_id)
);


 -- Workout Data ---------------------------------------------------------------
CREATE TABLE IF NOT EXISTS exercise
(
    exercise_id SMALLINT UNSIGNED AUTO_INCREMENT,
    name VARCHAR(20 NOT NULL,
    muscle_group VARCHAR(20),
    rep_type ENUM('count', 'distance', 'duration'),
    CONSTRAINT pk_exercise_id PRIMARY KEY (exercise_id)
);


CREATE TABLE IF NOT EXISTS working_set
(
    set_id SMALLINT UNSIGNED AUTO_INCREMENT,
    exercise_id SMALLINT UNSIGNED,
    person_id SMALLINT UNSIGNED,
    entry_date DATE NOT NULL,
    set_type VARCHAR(20),
    weight FLOAT NOT NULL,
    reps FLOAT NOT NULL,
    CONSTRAINT pk_set_id PRIMARY KEY (set_id),
    CONSTRAINT fk_person_id FOREIGN KEY (person_id) REFERENCES person (person_id)
    CONSTRAINT fk_exercise_id FOREIGN KEY (exercise_id) REFERENCES exercise (exercise_id)
);

