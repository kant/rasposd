#ifndef FILEIO_H
#define FILEIO_H

#include <QObject>
#include <QStringList>

#include <QQmlApplicationEngine>
#include <QQmlComponent>

class FileIO : public QObject
{
    Q_OBJECT

public:
    Q_PROPERTY(QString source
               READ source
               WRITE setSource
               NOTIFY sourceChanged)
    explicit FileIO(QObject *parent = 0);


    enum FlightData {
        TIME = 0,
        PITCH = 1,
        ROLL = 2,
        YAW = 3,
        SPEED = 7,
        TEMPERATURE = 10,
        PRESSURE = 11
    };
    Q_ENUMS(FlightData)

    static void declareQML() {
        qmlRegisterType<FileIO, 1>("FileIO", 1, 0, "FileIO");
    }

    Q_INVOKABLE void read();
    Q_INVOKABLE void getLastLinesFromFile();
    Q_INVOKABLE QString getValue(FlightData parameter);
    Q_INVOKABLE bool write(const QString& data);

    QString source() { return mSource; };


public slots:
    void setSource(const QString& source) { mSource = source; };

signals:
    void sourceChanged(const QString& source);
    void error(const QString& msg);

private:
    QString mSource;
    QStringList lastFileLine;

    int i;

};

#endif // FILEIO_H
