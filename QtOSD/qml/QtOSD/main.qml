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

    property double pitch_max: 3.5
    property double pitch_min: -3.5

    property int horizon_max_offset: 200

    property int font_size: 15

    property string text_color: "white"
    property string text_outline_color: "black"

    property string text_font: "arial"

    property int refresh_interval: 20

    property bool sim: false

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

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 10
    }

    Text {
        id: lblLatitude
        text: "Latitude"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.right: parent.horizontalCenter
        anchors.top: parent.top
        anchors.margins: 10
    }

    Text {
        id: lblLongitude
        text: "/ Longitude"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.left: parent.horizontalCenter
        anchors.top: parent.top
        anchors.margins: 10
    }


    Text {
        id: lblDate
        text: "2014.05.13"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight

        anchors.right: lblDateSep.left
        anchors.bottom: parent.bottom
        anchors.margins: 10
    }

    Text {
        id: lblDateSep
        text: "-"

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        horizontalAlignment: Text.AlignRight

        anchors.right: lblHeure.left
        anchors.bottom: parent.bottom
        anchors.margins: 10
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
        anchors.margins: 10
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

        property int step: 5
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

        if(sim) {
            data.incrementCurrentSimTime(refresh_interval/1000)
        } else {
            data.readLastLine();
        }

        horizon.rotation = parseFloat(data.getValue(FileIO.ROLL))
        pitch = -(Math.atan(parseFloat(data.getValue(FileIO.PITCH))/40)*horizon_max_offset)


        velocity_ruler.value = parseFloat(data.getValue(FileIO.SPEED));
        altitude_ruler.value = parseFloat(data.getValue(FileIO.ALTITUDE));
        direction_ruler.value = parseFloat(data.getValue(FileIO.YAW))


        lblTemperature.text = data.getValue(FileIO.TEMPERATURE) + "°C";

        lblLongitude.text = parseFloat(data.getValue(FileIO.LONGITUDE))
        lblLatitude.text = parseFloat(data.getValue(FileIO.LATITUDE))

        var date = new Date(data.getValue(FileIO.TIME)*1000);
        lblDate.text = date.getDate() + "." + date.getMonth() + "." + date.getFullYear()
        lblHeure.text = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()
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

//        source: "/home/pi/pilotage-fpv/recorder/records/last/data_pos.csv"
        source: "/home/pi/testing/recorder/records/last/data_pos.csv"
//        source: "/home/oswin/projects/pilotage-fpv/recorder/records/last/data_pos.csv"
//        source: "/home/oswin/projects/pilotage-fpv/recorder/records/velo_plaisante.csv"
//        DataType: LIVE

        onError: console.log(msg)
    }

    Component.onCompleted: {
        data.open();

        direction_ruler.labels = directionLabels();
    }

    Timer {
        interval: refresh_interval
        onTriggered: refresh()
        repeat: true
        running: true
    }

    Timer {
        interval: refresh_interval/2
        onTriggered: data.readNextLine()
        repeat: true
        running: sim
    }
}
