from mirion import create_app

if __name__ == "__main__":
    app = create_app('config.Config')
    app.run(host='127.0.0.1', port=5500, debug=True)
