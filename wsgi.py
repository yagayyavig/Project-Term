from app import create_app, create_tables

app = create_app()
create_tables(app)
