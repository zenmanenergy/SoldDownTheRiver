import uuid
from datetime import datetime
from _Lib.Database import ConnectToDatabase

def import_references():
    cursor, connection = ConnectToDatabase()
    try:
        # 1. Select distinct shipVoyageId, referenceScan
        cursor.execute("""
            SELECT DISTINCT shipVoyageId, referenceScan
            FROM solddowntheriver.raw_manifest
            ORDER BY shipVoyageId
        """)
        rows = cursor.fetchall()

        for row in rows:
            shipVoyageId = row[0]
            referenceScan = row[1] or ''
            reference_id = str(uuid.uuid4())
            now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

            # 2. Insert into reference
            cursor.execute("""
                INSERT INTO reference (ReferenceId, URL, Notes, dateUpdated)
                VALUES (%s, %s, %s, %s)
            """, (reference_id, '', referenceScan, now))

            # 3. Insert into referencelinks
            cursor.execute("""
                INSERT INTO referencelinks (ReferenceId, LinkId, TargetType, dateUpdated)
                VALUES (%s, %s, %s, %s)
            """, (reference_id, shipVoyageId, 'voyage', now))

        connection.commit()
        print(f"Imported {len(rows)} references.")
    except Exception as e:
        connection.rollback()
        print("Error:", e)
    finally:
        connection.close()

if __name__ == "__main__":
    import_references()
