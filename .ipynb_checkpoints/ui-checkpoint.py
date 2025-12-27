import streamlit as st
import pickle
import numpy as np

# -------------------------------
# Load model
# -------------------------------
model = pickle.load(open("model.pkl", "rb"))

# -------------------------------
# App UI
# -------------------------------
st.set_page_config(page_title="Car Price Predictor", layout="centered")
st.title("🚗 Car Price Predictor App")
st.write("Enter the car details to predict its price")

# -------------------------------
# Input Fields
# -------------------------------
year = st.number_input("Car Year", min_value=1990, max_value=2025, value=2015)
km_driven = st.number_input("Kilometers Driven", min_value=0, value=50000)
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
seller = st.selectbox("Seller Type", ["Individual", "Dealer"])
transmission = st.selectbox("Transmission", ["Manual", "Automatic"])
owner = st.selectbox("Owner Type", ["First", "Second", "Third"])

# -------------------------------
# Encoding (map strings to numbers)
# -------------------------------
fuel_map = {"Petrol": 0, "Diesel": 1, "CNG": 2}
seller_map = {"Individual": 0, "Dealer": 1}
trans_map = {"Manual": 0, "Automatic": 1}
owner_map = {"First": 0, "Second": 1, "Third": 2}

# -------------------------------
# Predict Button
# -------------------------------
if st.button("Predict Price"):
    input_data = np.array([[year, km_driven,
                            fuel_map[fuel],
                            seller_map[seller],
                            trans_map[transmission],
                            owner_map[owner]]])
    
    predicted_price = model.predict(input_data)
    st.success(f"Estimated Car Price: ₹ {int(predicted_price[0])}")

