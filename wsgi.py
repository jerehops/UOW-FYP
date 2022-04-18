from app import init_app

app = init_app()

"""
: App Entry Point
"""
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=80)

