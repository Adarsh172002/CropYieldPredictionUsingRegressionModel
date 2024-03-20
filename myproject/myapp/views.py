from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.hashers import make_password


#---------------------------------------------------------------------->>>>>>>>>>>>>>
class SignupView(View):
    template_name = 'signup.html'
    success_url = reverse_lazy('login')

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, self.template_name, {'error': 'Passwords do not match'})

        if User.objects.filter(email=email).exists():
            return render(request, self.template_name, {'error': 'Email is already registered'})

        # Create new user
        user = User.objects.create_user(username=username, email=email, password=password)

        # Redirect to success URL
        return redirect(self.success_url)

#-------------------------------------------------------------------------->>>>>>>



class CustomLoginView(View):
    template_name = 'login.html'
    success_url = reverse_lazy('home')  # Redirect to home page after successful login

    def get(self, request):
        return render(request, self.template_name, {'username': '', 'password': ''})

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Perform validation
        if not username or not password:
            error_message = "Username and password are required."
            return render(request, self.template_name, {'username': username, 'password': '', 'error_message': error_message})

        user = authenticate(request, username=username, password=password)
        print("user------------------------------>>>>>>>>>>>>>",user)
        if user is not None:
            login(request, user)
            return redirect(self.success_url)
        else:
            error_message = "Invalid username or password."
            return render(request, self.template_name, {'username': username, 'password': '', 'error_message': error_message})


#---------------------------------------------------------------------->>>>>>>>



import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
import pickle
import numpy as np

# Load the trained model
with open('/home/adarsh.singh/decision_tree_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define a function to perform preprocessing
# Load the encoded features DataFrame
encoded_features_df = pd.read_csv('/home/adarsh.singh/encoded_features.csv')

# Define a function to preprocess user input data
def preprocess_input_data(average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, country, item):
    # Load the saved DataFrame with encoded features

    # Create a DataFrame with the input data
    input_data = pd.DataFrame({
        'average_rain_fall_mm_per_year': [average_rain_fall_mm_per_year],
        'pesticides_tonnes': [pesticides_tonnes],
        'avg_temp': [avg_temp],
        'Country': [country],
        'Item': [item]
    })

    # Convert 'Country' and 'Item' columns to categorical data type
    input_data['Country'] = input_data['Country'].astype('category')
    input_data['Item'] = input_data['Item'].astype('category')

    # Convert numerical columns to numeric type if they are not already
    numerical_columns = ['average_rain_fall_mm_per_year', 'pesticides_tonnes', 'avg_temp']
    for col in numerical_columns:
        if input_data[col].dtype == 'object':
            input_data[col] = pd.to_numeric(input_data[col], errors='coerce')

    # One-hot encode categorical variables
    input_data_encoded = pd.get_dummies(input_data, columns=['Country', 'Item'], prefix=['Country', 'Item'])

    # Get missing columns from the encoded features DataFrame
    missing_columns = list(set(encoded_features_df.columns) - set(input_data_encoded.columns))

    # Merge input data with missing columns from encoded features DataFrame
    input_data_merged = pd.concat([input_data_encoded, encoded_features_df[missing_columns]], axis=1)

    # Adjust 'Country' and 'Item' columns to match encoded format
    encoded_country = 'Country_' + country
    encoded_item = 'Item_' + item

    # Keep only the first matching row for each combination of 'Country' and 'Item'
    input_data_merged = input_data_merged.drop_duplicates(subset=[encoded_country, encoded_item], keep='first')
    input_data_merged2=input_data_merged[:1]
    print(input_data_merged2)
    # Apply feature scaling only to numerical features
    scaler = MinMaxScaler()
    input_data_scaled = scaler.fit_transform(input_data_merged2)
    print("Scaled data")
    print(input_data_scaled)

    return input_data_scaled



# In your view class
from django.shortcuts import render

class Homepageview(View):
    template_name = 'home.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        average_rain_fall_mm_per_year = float(request.POST.get('average_rain_fall'))
        pesticides_tonnes = float(request.POST.get('pesticides_tonnes'))
        avg_temp = float(request.POST.get('avg_temp'))
        country = request.POST.get('countryname')  # Prepend 'Country_' prefix
        item = request.POST.get('itemname')  # Prepend 'Item_' prefix

        # Preprocess the input data
        input_data_scaled = preprocess_input_data(average_rain_fall_mm_per_year, pesticides_tonnes, avg_temp, country, item)

        # Make predictions
        prediction = model.predict(input_data_scaled)

        # Render the template with the input data and prediction
        return render(request, self.template_name, {
            'average_rain_fall': average_rain_fall_mm_per_year,
            'pesticides_tonnes': pesticides_tonnes,
            'avg_temp': avg_temp,
            'countryname': country,
            'itemname': item,
            'prediction': prediction,
        })


    
    
    
    
    
    
    
    
    
    

    