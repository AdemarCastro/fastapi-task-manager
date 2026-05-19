from sqlalchemy import create_engine
from app.core.config import settings

def test_connection():
    try:
        # Usa a mesma URL configurada no seu .env
        engine = create_engine(settings.DATABASE_URL)
        with engine.connect() as conn:
            print("✅ Conexão com o banco de dados OK!")
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")

if __name__ == "__main__":
    test_connection()