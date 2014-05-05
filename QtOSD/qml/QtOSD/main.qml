import QtQuick 2.2
import FileIO 1.0

Rectangle {
    width: 1280
    height: 720

    property int altitude: 0
    property int yaw: 0
    property int pitch: 0
    property int roll: 0
    property int speed: 0

    property int font_size: 30

    color: "transparent"


    Text {
        id: lblTemperature
        font.pointSize: font_size
        text: "Temperature"
        horizontalAlignment: Text.AlignRight

    }







    Rectangle {
        id: horizon
        width: 300
        height: 5
        color: "red"
        anchors.centerIn: parent
        rotation: roll
    }





    Ruler {
        id: altitude_ruler
        width: 50
        height: 400

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: 400

        property int value: 834
        property int nb_big_slots: 5
        property int nb_small_slots: 5

        property int step: 50

        x: 330
        y: 160
    }


    Ruler {
        id: velocity_ruler
        width: 50
        height: 400

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -400


        property int value: 0
        property int nb_big_slots: 5
        property int nb_small_slots: 1

        property int step: 100

        x: 827
        y: 160
    }



    function refresh() {
        data_imu.read();

        //lblSpeed.text = data_imu.getValue(FileIO.SPEED) + " m/s";

        horizon.rotation = data_imu.getValue(FileIO.ROLL)*180;

        velocity_ruler.value += 1
        altitude_ruler.value += 1
    }

    FileIO {
        id: data_imu
        source: "data_imu.csv"
        onError: console.log(msg)
    }

    Component.onCompleted: {
        data_imu.read();
    }

    Timer {
        interval: 40 // 25 Hz
        onTriggered: refresh()
        repeat: true
        running: true
    }
}
