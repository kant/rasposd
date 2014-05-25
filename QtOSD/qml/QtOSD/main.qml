import QtQuick 2.2
import FileIO 1.0

Rectangle {
    width: 720
    height: 576

    property double altitude: 0
    property double yaw: 0
    property double pitch: 0
    property double roll: 0
    property double speed: 0

    property double roll_max: 2.5883750748
    property double roll_min: -3.7320618556

    property double pitch_max: 1.4
    property double pitch_min: -1.65

    property int font_size: 15

    property string text_color: "white"
    property string text_outline_color: "black"

    property string text_font: "arial"

    color: "transparent"

    // arial ne marche pas si je ne la charge pas avant.
//    FontLoader {
//        id: myfont
//        source: "/home/pi/pilotage-fpv/Arial.ttf"
//    }

    Text {
        id: lblTemperature

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color


        horizontalAlignment: Text.AlignRight
    }

    Text {
        id: lblLatitude
        text: "46.540386 N "

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.right: parent.horizontalCenter
    }

    Text {
        id: lblLongitude
        text: " 6.631568 E"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.left: parent.horizontalCenter
    }


    Text {
        id: lblDate
        text: "2014.05.13 - "

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight

        anchors.right: lblHeure.left
        anchors.bottom: parent.bottom
    }


    Text {
        id: lblHeure
        text: "13:37:23"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight

        anchors.right: parent.right
        anchors.bottom: parent.bottom
    }


    Rectangle {
        id: horizon

        // Position
        width: 300
        height:4
        anchors.centerIn: parent
        rotation: roll

        anchors.verticalCenterOffset: pitch

        // Aspect
        color: "#80008000"
        border.color: "#C0FFFFFF"
        border.width: 1
        // smooth: true // did not work
    }



    Ruler {
        id: altitude_ruler

        width: 30
        height: 300

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: 300

        property double value: 834
        property int nb_big_slots: 5
        property int nb_small_slots: 5

        property int step: 20

    }


    Ruler {
        id: velocity_ruler
        width: 30
        height: 300

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: -300

        rotation: 180

        property double value: 0
        property int nb_big_slots: 5
        property int nb_small_slots: 1

        property int step: 100
        property bool reversed: true

    }

    Ruler{
        id: direction_ruler

        width: 20
        height: 500

        anchors.centerIn: parent
        anchors.verticalCenterOffset: -150

        rotation: -90

        property double value: 0
        property int nb_big_slots: 5
        property int nb_small_slots: 1


        property int step: 45

        property double cycle: 360

        property variant labels
        property bool reversed: true
    }



    function refresh() {
        data.read();

        //lblSpeed.text = data_imu.getValue(FileIO.SPEED) + " m/s";

        horizon.rotation = (parseFloat(data.getValue(FileIO.ROLL))/(roll_max+Math.abs(roll_min)))*360;
        lblTemperature.text = data.getValue(FileIO.TEMPERATURE) + "°C";

//        velocity_ruler.value = parseFloat(data.getValue(FileIO.SPEED));
        velocity_ruler.value += 1;
//        altitude_ruler.value = parseFloat(data.getValue(FileIO.ALTITUDE));
        altitude_ruler.value += 1
        direction_ruler.value = data.getValue(FileIO.YAW)/6*360;
    }

    function directionLabels() {
        var labels = [];
        labels[0] = ' N ';
        labels[45] = 'NE';
        labels[90] = ' E ';
        labels[135] = 'SE';
        labels[180] = ' S ';
        labels[225] = 'SO';
        labels[270] = ' O ';
        labels[315] = 'NO';
        return labels;
    }

    FileIO {
        id: data

        source: "/home/oswin/projects/pilotage-fpv/recorder/records/last/data_pos.csv"
//        DataType: LIVE

        onError: console.log(msg)
    }

    Component.onCompleted: {
        data.open();
        data.read();

        direction_ruler.labels = directionLabels();
    }

    Timer {
        interval: 20 // 50 Hz
        onTriggered: refresh()
        repeat: true
        running: true
    }
}
