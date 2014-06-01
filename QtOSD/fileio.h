#ifndef FILEIO_H
#define FILEIO_H

#include <QObject>
#include <QStringList>
#include <QFile>

#include <QQmlApplicationEngine>
#include <QQmlComponent>

class FileIO : public QObject
{
    Q_OBJECT

public:
    Q_PROPERTY(QString source READ source WRITE setSource NOTIFY sourceChanged)
//    Q_PROPERTY(DataType data_type READ getDataType WRITE setDataType)
    Q_PROPERTY(double current_sim_time READ getCurrentSimTime WRITE setCurrentSimTime)

    explicit FileIO(QObject *parent = 0);

    enum FlightData {
        TIME = 0,
        PITCH = 1,
        ROLL = 2,
        YAW = 3,
        SPEED = 4,
        CLIMB = 5,
        LATITUDE = 6,
        LONGITUDE = 7,
        ALTITUDE = 8,
        TEMPERATURE = 9
    };
    Q_ENUMS(FlightData)

//    enum DataType {
//        LIVE,
//        REPLAY
//    };
//    Q_ENUMS(DataType)

    static void declareQML() {
        qmlRegisterType<FileIO, 1>("FileIO", 1, 0, "FileIO");
    }

    Q_INVOKABLE void open();
    Q_INVOKABLE void readNextLine();
    Q_INVOKABLE void readLastLine();
    Q_INVOKABLE QString getValue(FlightData parameter);
    Q_INVOKABLE void incrementCurrentSimTime(double step);
    Q_INVOKABLE bool write(const QString &data);

    QString source() { return mSource; }
//    DataType getDataType() { return dataType; }
    Q_INVOKABLE double getCurrentSimTime() { return currentSimTime; }


public slots:
    void setSource(const QString &source) { mSource = source; }
//    void setDataType(DataType mDataType) { dataType = mDataType; }
    void setCurrentSimTime(double current_sim_time) { currentSimTime = current_sim_time; }

signals:
    void sourceChanged(const QString &source);
    void error(const QString &msg);

private:
    QString mSource;
    QStringList currentLine, nextLine;
    QFile *file;
//    DataType dataType;
    double currentSimTime;

    bool reuse;

    int i;

};

#endif // FILEIO_H
