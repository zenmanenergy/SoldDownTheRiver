import uuid
from Lib import Database

def save_role(RoleId,Role):
    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    

    if RoleId:
        # If the role already exists, update the existing row
        query = "UPDATE Roles SET Role = %s WHERE RoleId = %s"
        values = (Role, RoleId)
    else:
        # If the role doesn't exist, create a new row with a new role ID
        role_id = str(uuid.uuid4())
        query = "INSERT INTO Roles (RoleId, Role) VALUES (%s,%s)"
        values = (role_id,Role,)

    # Execute the query and commit the changes
    cursor.execute(query, values)
    connection.commit()

    # Close the database connection
    connection.close()

    # Return the role as a JSON response
    return {'success': True, 'role': Role}
