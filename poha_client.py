import logging
import time
import paho.mqtt.client as mqtt

class MQTTClient(mqtt.Client):
    def __init__(self, cname, clean_session=False, QoS=1, **kwargs):
        """Client with default persistent connection."""
        super(MQTTClient, self).__init__(cname, clean_session, **kwargs)
        self.logger = logging.getLogger("Creating PAHO Client")
        self.last_pub_time=time.time()
        self.QoS = QoS
        self.topic_ack=[]
        self.run_flag=True
        self.subscribe_flag=False
        self.bad_connection_flag=False
        self.connected_flag=False
        self.disconnect_flag=False
        self.disconnect_time=0.0
        self.pub_msg_count=0
        self.devices=[]
    
    # Define event callbacks
    def on_connect(self, userdata, flags, rc):
        if rc == 0:
            self.connected_flag=True
            self.bad_connection_flag = True
            self.logger.info('Connected')
            topic = 'PRINTER/+'
            # Start subscribe, with QoS level 0
            self.subscribe(topic, self.QoS)
            self.logger.info('Subscribed to topic %s' % (topic))
        elif rc == 1:
            self.bad_connection_flag = True
            self.logger.error('Connection refused - incorrect protocol version')
        elif rc == 2:
            self.bad_connection_flag = True
            self.logger.error('Connection refused - invalid client identifiers')
        elif rc == 3:
            self.bad_connection_flag = True
            self.logger.error('Connection refused - server unavailable')
        elif rc == 4:
            self.bad_connection_flag = True
            self.logger.error('Connection refused - bad username or password')
        elif rc == 5:
            self.bad_connection_flag = True
            self.logger.error('Connection refused - not authorised')
        elif rc == 6-255:
            self.bad_connection_flag = True
            self.logger.error('Currently unused')
    
    def on_disconnect(self, userdata, rc):
        self.logger.info("disconnection code = "  +str(rc))
        self.connected_flag=False
        self.disconnect_flag=True
        self.disconnect_time = time.time()

    def on_message(self, obj, msg):
        id = int(msg.topic.split("/")[1])
        self.logger.info(f'Received message from ID: {id}, topic: {msg.topic}')
        # work with the msg.payload

    def on_publish(self, obj, mid):
        self.pub_msg_count += 1
        self.logger.info("on_publish mid: " + str(mid))
        pass

    def on_subscribe(self, obj, mid, granted_qos):
        self.subscribe_flag=True
        self.logger.info("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_unsubscribe(self, userdata, mid, properties, reasonCodes):
        self.subscribe_flag=False
        self.logger.info('UNSUBSCRIBED')

    def before_notify_callback(self, event):
        # event.user = {
        #     "client": os.getenv('CLIENT_ID'),
        #     "device": os.getenv('DEVICE_IP'),
        # }
        pass