import os
import rospkg
import rospy


from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget, QPushButton
from std_msgs.msg import Header
from geometry_msgs.msg import PoseStamped
from tf.transformations import quaternion_from_euler

rooms = {
    "Room A": [[0,0,0]],
    "Room B" :[[1,1,1]],
    "Room C" :[[0,1,0]]
}


class MyPlugin(Plugin):
    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        # Give QObjects reasonable names
        self.setObjectName('MyPlugin')
        rp = rospkg.RosPack()
        # rospy.init_node('room_manager', anonymous=True)
        self.room_publisher  = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        rate = rospy.Rate(10)

        # Process standalone plugin command-line arguments
        from argparse import ArgumentParser
        parser = ArgumentParser()
        # Add argument(s) to the parser.
        parser.add_argument("-q", "--quiet", action="store_true",
                            dest="quiet",
                            help="Put plugin in silent mode")
        args, unknowns = parser.parse_known_args(context.argv())
        if not args.quiet:
            print('arguments: ', args)
            print('unknowns: ', unknowns)

        # Create QWidget
        self._widget = QWidget()
        ui_file = os.path.join(rp.get_path('rqt_mapr'), 'resource', 'MyPlugin.ui')
        # Extend the widget with all attributes and children from UI file
        loadUi(ui_file, self._widget)
        # Give QObjects reasonable names
        self._widget.setObjectName('MAPR UI')

        if context.serial_number() > 1:
            self._widget.setWindowTitle(self._widget.windowTitle() + (' (%d)' % context.serial_number()))
        # Add widget to the user interface
        context.add_widget(self._widget)



        # Binding button functionality
        self._widget.RmA.pressed.connect(self.publish_rmA)
        self._widget.RmB.pressed.connect(self.publish_rmB)
        self._widget.RmC.pressed.connect(self.publish_rmC)
        self._widget.mapping.pressed.connect(self.launch_mapping)
        self._widget.deliv.pressed.connect(self.launch_delivery)

    
    def publish_rmA(self):
        room = rooms["Room A"]
        self.publish_room(room)

    def publish_rmB(self):
        room = rooms["Room B"]
        self.publish_room(room)

    def publish_rmC(self):
        room = rooms["Room C"]
        self.publish_room(room)

    def publish_room(self, room):
        room_msg = PoseStamped()
        room_msg.pose.position.x = room[0][0]
        room_msg.pose.position.y = room[0][1]
        room_msg.pose.position.z = room[0][2]
        room_msg.header.stamp = rospy.Time.now()
        room_msg.header.frame_id = 'map'

        self.room_publisher.publish(room_msg)
        
    def launch_mapping(self):
        os.system("roslaunch mapr mapr_gmapping.launch")

    def launch_delivery(self):
        os.system("roslaunch mapr_nav mapr_nav.launch")

    def shutdown_plugin(self):
        # TODO unregister all publishers here
        pass

    def save_settings(self, plugin_settings, instance_settings):
        # TODO save intrinsic configuration, usually using:
        # instance_settings.set_value(k, v)
        pass

    def restore_settings(self, plugin_settings, instance_settings):
        # TODO restore intrinsic configuration, usually using:
        # v = instance_settings.value(k)
        pass

    # def trigger_configuration(self):
        # Comment in to signal that the plugin has a way to configure
        # This will enable a setting button (gear icon) in each dock widget title bar
        # Usually used to open a modal configuration dialog