import os
import rospy
import rospkg

from qt_gui.plugin import Plugin
from python_qt_binding import loadUi
from python_qt_binding.QtWidgets import QWidget


class MyPlugin(Plugin):
    def __init__(self, context):
        super(MyPlugin, self).__init__(context)
        self.setObjectName("MyPlugin")

        self._widget = QWidget()
        ui_file = os.path.join(
            rospkg.RosPack().get_path("rqt_mapr"), "resource", "MyPlugin.ui"
        )
        loadUi(ui_file, self._widget)
        self._widget.setObjectName("MyPluginUi")

        if context.serial_number() > 1:
            self._widget.setWindowTitle(
                self._widget.windowTitle() + (" (%d)" % context.serial_number())
            )
        context.add_widget(self._widget)

    def shutdown_plugin(self):
        return super().shutdown_plugin()

    def save_settings(self, plugin_settings, instance_settings):
        return super().save_settings(plugin_settings, instance_settings)

    def restore_settings(self, plugin_settings, instance_settings):
        return super().restore_settings(plugin_settings, instance_settings)
