# This variable stores the next AddressID integer
next_adres_id = None
# This variable indicates whether the next_address_id has been initialized
next_adres_id_read = 0

# @brief This class is used to handle the Customer address in ODS 
# @note  There is not need to create an object of this class as all
#        methods in this class are static
class Adres :

    # @brief The function is used to insert the address details entered by the 
    #        customer in the mysql database
    # @param pysql Pysql Object
    # @param Name of the parameter are self-explanatory (string)
    # @retval boolean returns the 1 if the entry is successfully inserted in the 
    #         database, else 0
    @staticmethod
    def add_customer_adres(pysql, customer_id, pincode, street, landmark, city, state, addr_type) :

        # Fetch the global variables
        global next_adres_id
        global next_adres_id_read

        # Find the last address id stored in the database to allocate next id
        # to the next address. If the number of entries of the address are not
        # known, then using address_id_read flag and sql query, we can find it!
        if not next_adres_id_read :
            sql_stmt =  'SELECT COUNT(*) ' \
                        'FROM Adres'
            pysql.run(sql_stmt)
            next_adres_id = pysql.scalar_result
            next_adres_id_read = 1 

        # Now get the adres_id
        adres_id = format(next_adres_id, '06d')

        # Make an entry in the database
        sql_stmt =  'INSERT INTO Adres ' \
                    'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)' 

        try : 
            pysql.run(sql_stmt, (customer_id, adres_id, pincode, street, landmark, city, state, addr_type))

            # Commit the changes to the remote database
            pysql.commit()

            # Next address_id for further addition of address 
            next_adres_id += 1
            return 1 
        except :
            return 0

    @staticmethod
    def view_all_adres_of_customer(pysql, customer_id) :
            
        sql_stmt =  'SELECT Adres_ID, Pincode, Street, Landmark, City, State, Type ' \
                    'FROM Adres ' \
                    'WHERE Customer_ID = %s' \

        pysql.run(sql_stmt, (customer_id, ))
        adreses = pysql.result

        return adreses
