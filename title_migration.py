# from database import SessionLocal
from SQLORmodel import NameBasics, TitlePrincipals
# from sqlalchemy import create_engine, Se
# from sqlalchemy.orm import sessionmaker



from sqlalchemy import create_engine, insert, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# 1. Setup your engine (Update with your actual connection string)
engine = create_engine("postgresql+psycopg2://postgres:jrs%23321@localhost:5432/inapp_db")

# 2. Define SessionLocal - This was the missing piece!
SessionLocal = sessionmaker(bind=engine)

def migrate_known_for_titles(engine, batch_size=50000):
    total_inserted = 0
    buffer = []
    
    # Use a raw connection to stream 15M rows without session interference
    with engine.connect() as stream_conn:
        stream_conn = stream_conn.execution_options(stream_results=True)
        
        # Select only required columns for memory efficiency
        stmt = select(NameBasics.nconst, NameBasics.knownForTitles)
        result = stream_conn.execute(stmt).yield_per(batch_size)

        # Use the factory to create a dedicated writer session
        with SessionLocal() as write_session:
            for row in result:
                if not row.knownForTitles or row.knownForTitles == "\\N":
                    continue

                titles = row.knownForTitles.split(",")
                for t in titles:
                    t = t.strip()
                    if t:
                        buffer.append({
                            "tconst": t,
                            "nconst": row.nconst
                        })

                # Check if buffer is full
                if len(buffer) >= batch_size:
                    try:
                        write_session.execute(insert(TitlePrincipals), buffer)
                        write_session.commit()
                        total_inserted += len(buffer)
                        print(f"✅ Processed: {total_inserted} rows...")
                    except SQLAlchemyError as e:
                        print(f"❌ Batch error: {e}")
                        write_session.rollback()
                    finally:
                        buffer.clear()

            # Final flush for the last partial batch
            if buffer:
                try:
                    write_session.execute(insert(TitlePrincipals), buffer)
                    write_session.commit()
                    total_inserted += len(buffer)
                    print(f"🏁 Migration complete. Total inserted: {total_inserted}")
                except SQLAlchemyError as e:
                    print(f"❌ Final batch error: {e}")
                    write_session.rollback()

# Run the migration
if __name__ == "__main__":
    migrate_known_for_titles(engine)