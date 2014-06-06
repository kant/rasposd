import QtQuick 2.2
import FileIO 1.0

Rectangle {
    width: 720
    height: 576

    property double altitude: 0
    property double speed: 0
    property double temperature: 0

    property double yaw: 0
    property double pitch: 0
    property double roll: 0

    property int saved_angle: 0

    property int horizon_voffset: 0
    property int horizon_max_offset: 200

    property int font_size: 15

    property string text_color: "white"
    property string text_outline_color: "black"

    property string date: ""
    property string hour: ""

    property string source_file_path: "/home/pi/pilotage-fpv/recorder/records/last/data_pos.csv"

    property string text_font: "arial"

    property int refresh_interval: 20

    property bool sim: false

    property double start_longitude
    property double start_latitude

    property double longitude
    property double latitude

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

        text: temperature  + "°C"

        horizontalAlignment: Text.AlignRight

        anchors.right: parent.right
        anchors.top: parent.top
        anchors.margins: 10
    }

    Text {
        id: lblLongitude
        text: longitude

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
        id: lblLatitude
        text: latitude

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.left: lblLongitude.left
        anchors.top: lblLongitude.bottom
    }


    Text {
        id: lblStartLongitude
        text: start_longitude

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.left: parent.left
        anchors.top: parent.top
        anchors.margins: 10
    }

    Text {
        id: lblStartLatitude
        text: start_latitude

        font.pointSize: font_size
        font.family: text_font

        color: text_color
        style: Text.Outline;
        styleColor: text_outline_color

        anchors.left: lblStartLongitude.left
        anchors.top: lblStartLongitude.bottom
    }


    Text {
        id: lblDate
        text: date

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
        text: hour

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

        anchors.verticalCenterOffset: horizon_voffset

        // Aspect
        color: "#80008000"
        border.color: "#C0FFFFFF"
        border.width: 1
//        smooth: true // did not work
    }


    Rectangle {
        id: home_indicator

        width: 20
        height:2

        anchors.centerIn: parent

        // Aspect
        color: "#80008000"
        border.color: "#C0FFFFFF"
        border.width: 1
    }



    Ruler {
        id: altitude_ruler

        width: 30
        height: 300

        anchors.centerIn: parent
        anchors.horizontalCenterOffset: 300

        property double value: altitude
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
        property bool reversed: true

        property double value: yaw

        property int nb_big_slots: 5
        property int nb_small_slots: 1
        property int step: 45
        property double cycle: 360

        property variant labels
    }

    function refresh() {

        if(sim) {
            data.incrementCurrentSimTime(refresh_interval/1000)
        } else {
            data.readLastLine();
        }

        horizon.rotation = parseFloat(data.getValue(FileIO.ROLL))
        horizon_voffset = -(Math.atan(parseFloat(data.getValue(FileIO.PITCH))/40)*horizon_max_offset)


        velocity_ruler.value = parseFloat(data.getValue(FileIO.SPEED));
        altitude = parseFloat(data.getValue(FileIO.ALTITUDE));
        yaw = parseFloat(data.getValue(FileIO.YAW))


        temperature = parseFloat(data.getValue(FileIO.TEMPERATURE));

        longitude = parseFloat(data.getValue(FileIO.LONGITUDE))
        latitude = parseFloat(data.getValue(FileIO.LATITUDE))

        var currentDate = new Date(data.getValue(FileIO.TIME)*1000);
        date = currentDate.getDate() + "." + currentDate.getMonth() + "." + currentDate.getFullYear()
        hour = currentDate.getHours() + ":" + currentDate.getMinutes() + ":" + currentDate.getSeconds()

        var angle = Math.atan((latitude-start_latitude)/(longitude-start_longitude))-yaw/(180/Math.PI);
        home_indicator.rotation = angle*180/Math.PI
        home_indicator.anchors.verticalCenterOffset = 150*Math.sin(angle);
        home_indicator.anchors.horizontalCenterOffset = 150*Math.cos(angle);
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
        source: source_file_path
        onError: console.log(msg)
    }

    Component.onCompleted: {
        data.open();
        data.readLastLine();

        direction_ruler.labels = directionLabels();

        start_longitude = parseFloat(data.getValue(FileIO.LONGITUDE))
        start_latitude = parseFloat(data.getValue(FileIO.LATITUDE))
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
