
import streamlit as st
import pickle
import pandas as pd
import numpy as np

# -------------------------------
# 1. LOAD THE TRAINED MODEL
# -------------------------------
# Ensure 'carpricepredication_model.pkl' is in the same folder as this script
model = pickle.load(open("carpricepredication_model.pkl", "rb"))

# -------------------------------
# 2. SETUP DATA & COLUMNS
# -------------------------------

# The exact 34 columns your model was trained on (Must match order exactly)
model_columns = [
    'year', 'mileage', 'tax', 'mpg', 'engineSize', 'model_ C-MAX',
    'model_ EcoSport', 'model_ Edge', 'model_ Escort', 'model_ Fiesta',
    'model_ Focus', 'model_ Fusion', 'model_ Galaxy', 'model_ Grand C-MAX',
    'model_ Grand Tourneo Connect', 'model_ KA', 'model_ Ka+',
    'model_ Kuga', 'model_ Mondeo', 'model_ Mustang', 'model_ Puma',
    'model_ Ranger', 'model_ S-MAX', 'model_ Streetka',
    'model_ Tourneo Connect', 'model_ Tourneo Custom',
    'model_ Transit Tourneo', 'model_Focus', 'transmission_Manual',
    'transmission_Semi-Auto', 'fuelType_Electric', 'fuelType_Hybrid',
    'fuelType_Other', 'fuelType_Petrol'
]

# Real average values from your dataset (Tax, MPG, EngineSize)
# Used to auto-fill the technical specs for the user
default_stats = {
    'B-MAX': {'tax': 91, 'mpg': 55.7, 'engine': 1.3},
    'C-MAX': {'tax': 72, 'mpg': 59.5, 'engine': 1.4},
    'EcoSport': {'tax': 136, 'mpg': 53.1, 'engine': 1.1},
    'Edge': {'tax': 157, 'mpg': 46.2, 'engine': 2.0},
    'Escort': {'tax': 265, 'mpg': 34.4, 'engine': 1.8},
    'Fiesta': {'tax': 101, 'mpg': 61.0, 'engine': 1.1},
    'Focus': {'tax': 111, 'mpg': 60.1, 'engine': 1.4},
    'Fusion': {'tax': 184, 'mpg': 45.4, 'engine': 1.5},
    'Galaxy': {'tax': 146, 'mpg': 53.3, 'engine': 2.0},
    'Grand C-MAX': {'tax': 73, 'mpg': 58.4, 'engine': 1.4},
    'Grand Tourneo Connect': {'tax': 114, 'mpg': 60.2, 'engine': 1.5},
    'KA': {'tax': 56, 'mpg': 56.1, 'engine': 1.2},
    'Ka+': {'tax': 135, 'mpg': 53.3, 'engine': 1.2},
    'Kuga': {'tax': 146, 'mpg': 51.7, 'engine': 1.8},
    'Mondeo': {'tax': 100, 'mpg': 60.0, 'engine': 1.9},
    'Mustang': {'tax': 211, 'mpg': 24.3, 'engine': 4.4},
    'Puma': {'tax': 148, 'mpg': 50.1, 'engine': 1.0},
    'Ranger': {'tax': 240, 'mpg': 28.3, 'engine': 3.2},
    'S-MAX': {'tax': 150, 'mpg': 51.9, 'engine': 2.0},
    'Streetka': {'tax': 280, 'mpg': 35.6, 'engine': 1.6},
    'Tourneo Connect': {'tax': 109, 'mpg': 58.1, 'engine': 1.5},
    'Tourneo Custom': {'tax': 164, 'mpg': 38.6, 'engine': 2.0},
    'Transit Tourneo': {'tax': 235, 'mpg': 42.2, 'engine': 2.2},
    'Other': {'tax': 120, 'mpg': 55.0, 'engine': 1.5} # Fallback
}

# -------------------------------
# 3. STREAMLIT APP UI
# -------------------------------
st.set_page_config(page_title="Car Price Predictor", layout="centered")
st.title("🚗 Car Price Predictor App")

# --- Initialize Session State ---
# This allows the "Auto-Fill" button to update the input boxes dynamically
if 'tax_val' not in st.session_state: st.session_state['tax_val'] = 150
if 'mpg_val' not in st.session_state: st.session_state['mpg_val'] = 55.0
if 'eng_val' not in st.session_state: st.session_state['eng_val'] = 1.5

# --- Main Input Section ---
col1, col2 = st.columns(2)

with col1:
    year = st.number_input("Car Year", 1990, 2025, 2018)
    mileage = st.number_input("Mileage", 0, 300000, 40000)
    
    # All available models from your dataset
    car_model = st.selectbox("Car Model", [
        'B-MAX', 'C-MAX', 'EcoSport', 'Edge', 'Escort', 'Fiesta', 'Focus', 
        'Fusion', 'Galaxy', 'Grand C-MAX', 'Grand Tourneo Connect', 'KA', 
        'Ka+', 'Kuga', 'Mondeo', 'Mustang', 'Puma', 'Ranger', 'S-MAX', 
        'Streetka', 'Tourneo Connect', 'Tourneo Custom', 'Transit Tourneo'
    ])

with col2:
    transmission = st.selectbox("Transmission", ["Manual", "Semi-Auto", "Automatic"])
    fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "Electric", "Hybrid", "Other"])
    
    st.write("") # Spacer
    st.write("") # Spacer
    
    # BUTTON: Auto-Fill Defaults
    if st.button("🔄 Auto-Fill Specs", help="Click to fill Tax, MPG, and Engine based on model average"):
        stats = default_stats.get(car_model, default_stats['Other'])
        st.session_state['tax_val'] = int(stats['tax'])
        st.session_state['mpg_val'] = float(stats['mpg'])
        st.session_state['eng_val'] = float(stats['engine'])
        st.rerun() # Refresh app to show new numbers

st.markdown("---")
st.subheader("Technical Specs")
st.caption("You can adjust these manually or use the Auto-Fill button above.")

# --- Secondary Input Section (Technical) ---
c1, c2, c3 = st.columns(3)
# These inputs are linked to st.session_state so the button can change them
tax = c1.number_input("Road Tax (£)", min_value=0, key='tax_val')
mpg = c2.number_input("MPG", min_value=0.0, key='mpg_val')
engineSize = c3.number_input("Engine Size (L)", min_value=0.0, step=0.1, key='eng_val')

st.markdown("---")

# -------------------------------
# 4. PREDICTION LOGIC
# -------------------------------
if st.button("Predict Price", type="primary"):
    
    # A. Initialize a dictionary with all 34 columns set to 0
    input_data = {col: 0 for col in model_columns}
    
    # B. Set the numeric values
    input_data['year'] = year
    input_data['mileage'] = mileage
    input_data['tax'] = tax
    input_data['mpg'] = mpg
    input_data['engineSize'] = engineSize
    
    # C. Handle One-Hot Encoding (Setting the correct flags to 1)
    
    # 1. Car Model
    model_key = f"model_ {car_model}"
    if model_key in input_data:
        input_data[model_key] = 1
    elif car_model == 'Focus': # Special handling for Focus if needed (due to potential typo in training columns)
         if 'model_Focus' in input_data: input_data['model_Focus'] = 1

    # 2. Transmission
    if transmission == "Manual":
        input_data['transmission_Manual'] = 1
    elif transmission == "Semi-Auto":
        input_data['transmission_Semi-Auto'] = 1
    # If Automatic, both remain 0 (assuming it was dropped during training as reference)
    
    # 3. Fuel Type
    fuel_key = f"fuelType_{fuel}"
    if fuel_key in input_data:
        input_data[fuel_key] = 1
        
    # D. Create DataFrame
    df_input = pd.DataFrame([input_data])
    
    # E. Predict
    try:
        prediction = model.predict(df_input)
        result = int(prediction[0])
        st.balloons()
        st.success(f"### Estimated Price: ₹ {result:,}")
    except Exception as e:
        st.error(f"Error during prediction: {e}")