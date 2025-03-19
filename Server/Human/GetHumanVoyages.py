from _Lib import Database

def get_human_voyages(HumanId):
    if not HumanId:
        HumanId = "-1"

    # Connect to the database
    cursor, connection = Database.ConnectToDatabase()

    # Construct the SQL query
    query = """
        SELECT DISTINCT
            voyagehumans.VoyageId,
            voyagehumans.RoleId,
            voyagehumans.Notes,
            voyagehumans.SellingSlaveTraderHumanId,
            selling_humans.FirstName AS SellingSlaveTraderFirstName,
            selling_humans.LastName AS SellingSlaveTraderLastName,
            voyagehumans.BuyingSlaveTraderHumanId,
            buying_humans.FirstName AS BuyingSlaveTraderFirstName,
            buying_humans.LastName AS BuyingSlaveTraderLastName,
            voyagehumans.ShippingAgentHumanId,
            shipping_humans.FirstName AS ShippingAgentFirstName,
            shipping_humans.LastName AS ShippingAgentLastName,
            voyagehumans.CollectingAgentHumanId,
            collecting_humans.FirstName AS CollectingAgentFirstName,
            collecting_humans.LastName AS CollectingAgentLastName
        FROM voyagehumans
        LEFT JOIN humans AS selling_humans ON voyagehumans.SellingSlaveTraderHumanId = selling_humans.HumanId
        LEFT JOIN humans AS buying_humans ON voyagehumans.BuyingSlaveTraderHumanId = buying_humans.HumanId
        LEFT JOIN humans AS shipping_humans ON voyagehumans.ShippingAgentHumanId = shipping_humans.HumanId
        LEFT JOIN humans AS collecting_humans ON voyagehumans.CollectingAgentHumanId = collecting_humans.HumanId
        WHERE voyagehumans.HumanId = '{}'
           OR voyagehumans.SellingSlaveTraderHumanId = '{}'
           OR voyagehumans.BuyingSlaveTraderHumanId = '{}'
           OR voyagehumans.ShippingAgentHumanId = '{}'
           OR voyagehumans.CollectingAgentHumanId = '{}'
        ORDER BY voyagehumans.VoyageId ASC
    """.format(HumanId, HumanId, HumanId, HumanId, HumanId)

    # Print the SQL query with the actual HumanId value
    print(query)

    # Execute the query and get the results
    cursor.execute(query)
    result = cursor.fetchall()
    if not result:
        result = []

    # Close the database connection
    connection.close()

    # Return the result as a dictionary
    return result
