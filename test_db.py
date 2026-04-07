from app import create_app, db

app = create_app()

with app.app_context():
    try:
        # Teste simples: executar uma consulta
        result = db.session.execute(db.text("SELECT 1")).fetchone()
        if result:
            print("Conexão com o banco de dados bem-sucedida!")
        else:
            print("Falha na conexão: consulta não retornou resultado.")
    except Exception as e:
        print(f"Falha na conexão com o banco de dados: {e}")
    finally:
        db.session.close()