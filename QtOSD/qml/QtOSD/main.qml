import QtQuick 2.2
import FileIO 1.0

Rectangle {
    width: 1280
    height: 720

    property double altitude: 0
    property double yaw: 0
    property double pitch: 0
    property double roll: 0
    property double speed: 0

    property double roll_max: 2.5883750748
    property double roll_min: -3.7320618556


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

    }

    Ruler{
        id: direction_ruler
        width: 50
        height: 400

        anchors.centerIn: parent
        anchors.verticalCenterOffset: -200

        rotation: -90

        property double value: 0
        property int nb_big_slots: 5
        property int nb_small_slots: 1

        property int step: 100
    }



    function refresh() {
        data_imu.read();

        //lblSpeed.text = data_imu.getValue(FileIO.SPEED) + " m/s";

        horizon.rotation = (parseFloat(data_imu.getValue(FileIO.ROLL))/(roll_max+Math.abs(roll_min)))*360;
        lblTemperature.text = data_imu.getValue(FileIO.TEMPERATURE) + "°C";

        velocity_ruler.value += 1
        altitude_ruler.value = parseFloat(data_imu.getValue(FileIO.PRESSURE));
        direction_ruler.value = data_imu.getValue(FileIO.YAW)/6*360;
    }

    FileIO {
        id: data_imu
        source: "data_imu_live.csv"
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
