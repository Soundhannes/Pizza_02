-- Pizza Calculator Database Schema

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS pizza_calculator;
USE pizza_calculator;

-- Pizza Styles Table
CREATE TABLE pizza_styles (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    typical_hydration DECIMAL(5,2) DEFAULT 65.00,
    typical_salt_percentage DECIMAL(4,2) DEFAULT 2.00,
    typical_yeast_percentage DECIMAL(4,2) DEFAULT 0.25,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Preferment Methods Table
CREATE TABLE preferment_methods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    typical_percentage DECIMAL(5,2) DEFAULT 20.00,
    fermentation_time_hours INT DEFAULT 12,
    temperature_celsius INT DEFAULT 20,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Recipes Table
CREATE TABLE recipes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200) NOT NULL,
    pizza_style_id INT NOT NULL,
    preferment_method_id INT,
    flour_weight DECIMAL(8,2) NOT NULL,
    water_percentage DECIMAL(5,2) NOT NULL,
    salt_percentage DECIMAL(4,2) NOT NULL,
    yeast_percentage DECIMAL(4,2) NOT NULL,
    preferment_percentage DECIMAL(5,2) DEFAULT 0.00,
    oil_percentage DECIMAL(4,2) DEFAULT 0.00,
    sugar_percentage DECIMAL(4,2) DEFAULT 0.00,
    fermentation_time_hours INT DEFAULT 24,
    fermentation_temperature INT DEFAULT 20,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (pizza_style_id) REFERENCES pizza_styles(id) ON DELETE RESTRICT,
    FOREIGN KEY (preferment_method_id) REFERENCES preferment_methods(id) ON DELETE SET NULL
);

-- Calculations Table
CREATE TABLE calculations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    recipe_id INT NOT NULL,
    number_of_pizzas INT NOT NULL,
    pizza_weight DECIMAL(8,2) NOT NULL,
    total_flour DECIMAL(8,2) NOT NULL,
    total_water DECIMAL(8,2) NOT NULL,
    total_salt DECIMAL(8,2) NOT NULL,
    total_yeast DECIMAL(8,2) NOT NULL,
    total_oil DECIMAL(8,2) DEFAULT 0.00,
    total_sugar DECIMAL(8,2) DEFAULT 0.00,
    preferment_flour DECIMAL(8,2) DEFAULT 0.00,
    preferment_water DECIMAL(8,2) DEFAULT 0.00,
    preferment_yeast DECIMAL(8,2) DEFAULT 0.00,
    main_dough_flour DECIMAL(8,2) NOT NULL,
    main_dough_water DECIMAL(8,2) NOT NULL,
    main_dough_salt DECIMAL(8,2) NOT NULL,
    main_dough_yeast DECIMAL(8,2) NOT NULL,
    calculated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- Widgets Table
CREATE TABLE widgets (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    widget_type ENUM('calculator', 'converter', 'timer', 'reference') NOT NULL,
    configuration JSON,
    is_active BOOLEAN DEFAULT TRUE,
    display_order INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create Indexes for Performance

-- Pizza Styles Indexes
CREATE INDEX idx_pizza_styles_name ON pizza_styles(name);

-- Preferment Methods Indexes
CREATE INDEX idx_preferment_methods_name ON preferment_methods(name);

-- Recipes Indexes
CREATE INDEX idx_recipes_name ON recipes(name);
CREATE INDEX idx_recipes_pizza_style ON recipes(pizza_style_id);
CREATE INDEX idx_recipes_preferment_method ON recipes(preferment_method_id);
CREATE INDEX idx_recipes_created_at ON recipes(created_at);

-- Calculations Indexes
CREATE INDEX idx_calculations_recipe ON calculations(recipe_id);
CREATE INDEX idx_calculations_calculated_at ON calculations(calculated_at);
CREATE INDEX idx_calculations_recipe_pizzas ON calculations(recipe_id, number_of_pizzas);

-- Widgets Indexes
CREATE INDEX idx_widgets_type ON widgets(widget_type);
CREATE INDEX idx_widgets_active ON widgets(is_active);
CREATE INDEX idx_widgets_display_order ON widgets(display_order);
CREATE INDEX idx_widgets_type_active ON widgets(widget_type, is_active);

-- Insert Default Data

-- Default Pizza Styles
INSERT INTO pizza_styles (name, description, typical_hydration, typical_salt_percentage, typical_yeast_percentage) VALUES
('Neapolitan', 'Traditional Neapolitan pizza with high hydration', 65.00, 2.50, 0.25),
('New York Style', 'Thin crust New York style pizza', 60.00, 2.00, 0.50),
('Sicilian', 'Thick crust Sicilian style pizza', 65.00, 2.00, 1.00),
('Roman', 'Thin and crispy Roman style pizza', 70.00, 2.50, 0.30),
('Chicago Deep Dish', 'Thick crust Chicago style pizza', 55.00, 2.00, 1.50);

-- Default Preferment Methods
INSERT INTO preferment_methods (name, description, typical_percentage, fermentation_time_hours, temperature_celsius) VALUES
('Poolish', 'Equal parts flour and water with small amount of yeast', 20.00, 12, 20),
('Biga', 'Stiff Italian preferment with low hydration', 25.00, 16, 18),
('Sourdough Starter', 'Natural fermentation starter', 15.00, 24, 22),
('Sponge', 'Soft preferment with higher hydration', 30.00, 8, 25);

-- Default Widgets
INSERT INTO widgets (name, widget_type, configuration, is_active, display_order) VALUES
('Pizza Calculator', 'calculator', '{"default_pizzas": 4, "default_weight": 250}', TRUE, 1),
('Hydration Converter', 'converter', '{"conversion_types": ["percentage_to_grams", "grams_to_percentage"]}', TRUE, 2),
('Fermentation Timer', 'timer', '{"default_hours": 24, "temperature_adjustment": true}', TRUE, 3),
('Ingredient Reference', 'reference', '{"categories": ["flour", "yeast", "salt", "water"]}', TRUE, 4);