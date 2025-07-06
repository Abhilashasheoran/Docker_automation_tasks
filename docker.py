import streamlit as st
import os
import subprocess
from sklearn.linear_model import LinearRegression
import numpy as np

# --------- MARKS PREDICTION ---------
def predict_marks(hours):
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([50, 60, 65, 70, 80])
    model = LinearRegression()
    model.fit(X, y)
    return model.predict([[hours]])[0]

# --------- DOCKER FILE CREATIONS ---------
def create_flask_dockerfile():
    with open("Dockerfile_flask", "w") as f:
        f.write('''FROM python:3.9
WORKDIR /app
COPY app.py /app
RUN pip install flask scikit-learn numpy
CMD ["python", "app.py"]''')

    with open("app.py", "w") as f:
        f.write('''from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)

def predict_marks(hours):
    X = np.array([[1], [2], [3], [4], [5]])
    y = np.array([50, 60, 65, 70, 80])
    model = LinearRegression()
    model.fit(X, y)
    return model.predict([[hours]])[0]

@app.route('/predict', methods=['GET'])
def predict():
    try:
        hours = float(request.args.get("hours", 0))
        result = predict_marks(hours)
        return jsonify({"predicted_marks": result})
    except:
        return jsonify({"error": "Invalid input"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')''')

def create_apache_dockerfile():
    os.makedirs("apache_html", exist_ok=True)
    with open("apache_html/index.html", "w") as f:
        f.write("<h1>Welcome to Apache Server in Docker!</h1>")

    with open("Dockerfile_apache", "w") as f:
        f.write('''FROM httpd:latest
COPY ./apache_html/ /usr/local/apache2/htdocs/''')

def create_dind_dockerfile():
    with open("Dockerfile_dind", "w") as f:
        f.write('FROM docker:dind\nCMD ["dockerd-entrypoint.sh"]')

# --------- STREAMLIT UI ---------
st.set_page_config(page_title="Docker Menu Project", page_icon="🐳")
st.title("🐳 Docker Menu Project (Streamlit Edition)")
st.markdown("Use this web app to run common Docker-based automation tasks.")

# --------- SECTION 1: ML Prediction ---------
st.subheader("📊 Predict Student Marks")
hours = st.number_input("Enter hours studied:", min_value=0.0, step=0.5)
if st.button("Predict Marks"):
    result = predict_marks(hours)
    st.success(f"Predicted Marks: {round(result, 2)}")

# --------- SECTION 2: Flask API in Docker ---------
st.subheader("🌐 Flask API in Docker")
if st.button("Build & Run Flask API Container"):
    create_flask_dockerfile()
    os.system("docker build -t flask-api -f Dockerfile_flask .")
    os.system("docker run -d -p 5000:5000 flask-api")
    st.success("Flask API container is running at port 5000.")

# --------- SECTION 3: Docker-in-Docker ---------
st.subheader("📦 Docker-in-Docker")
if st.button("Launch Docker-in-Docker Container"):
    create_dind_dockerfile()
    os.system("docker build -t docker-dind -f Dockerfile_dind .")
    os.system("docker run --privileged -d docker-dind")
    st.success("Docker-in-Docker container launched.")

# --------- SECTION 4: Firefox ---------
st.subheader("🦊 Launch Firefox in Docker")
if st.button("Run Firefox Container"):
    os.system("docker run -d -p 5800:5800 jlesage/firefox")
    st.success("Firefox is running. Access via VNC at port 5800.")

# --------- SECTION 5: VLC ---------
st.subheader("🎞️ Launch VLC in Docker")
if st.button("Run VLC Container"):
    os.system("docker run -d -p 5801:5800 jlesage/vlc")
    st.success("VLC is running. Access via VNC at port 5801.")

# --------- SECTION 6: Apache Server ---------
st.subheader("🌐 Apache Web Server in Docker")
if st.button("Build & Launch Apache Server"):
    create_apache_dockerfile()
    os.system("docker build -t my-apache -f Dockerfile_apache .")
    os.system("docker run -dit --name apache-server -p 8080:80 my-apache")
    st.success("Apache server is running at port 8080.")

# --------- FOOTER ---------
st.markdown("---")
st.caption("Made with ❤️ using Streamlit & Docker")
