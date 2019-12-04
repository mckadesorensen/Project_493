from project_493 import app

if __name__ == "__main__":
    app.run(debug=True, ssl_context=('cert.pem', 'key.pem'))
