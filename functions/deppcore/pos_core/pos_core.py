import dac_code
import com_msg


def get_all_store_locations():
    sqlcode = "SELECT stores.store_autoid, stores.store_name, stores.store_shortcode  FROM fred.stores stores"
    result = dac_code.dbreadquery_sql(sqlcode)
    return result

def add_store_location(para):
    callingfunction="store_location_added"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload="")
    pass


def update_store_location(para):
    callingfunction="store_location_updated"
    com_msg.make_mqtt_call(topic=str(callingfunction), payload="")
    pass
