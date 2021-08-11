from mirion import create_app

if __name__ == "__main__":
    app = create_app('config.Config')
    app.run(host='0.0.0.0', port=5500, debug=True)
