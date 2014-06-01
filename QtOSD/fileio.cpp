#include "fileio.h"
#include <QFile>
#include <QTextStream>
#include <QDebug>

#include <limits>

FileIO::FileIO(QObject *parent) :
    QObject(parent)
{
    reuse = false;
}

void FileIO::open()
{
    if (mSource.isEmpty()){
        emit error("source is empty");
    }

    file = new QFile(mSource);

    if (!file->exists())
        emit error("file doesn't exist...");

    file->open(QIODevice::ReadOnly);

    file->readLine(); // Skip header


    currentSimTime = std::numeric_limits<double>::max();

    readNextLine(); // First datas
    currentSimTime = currentLine.value(TIME).toDouble();
}

void FileIO::readLastLine()
{

    file->seek(file->size()-1);

    int count = 0;

    while ( (count < 2) && (file->pos() > 0) )
    {
        char ch;
        file->getChar(&ch);
        file->seek(file->pos()-2); /// minus 2 because getch moves one forward

        if (ch == '\n')
            count++;
    }

    QString r = file->readAll();

    currentLine = r.split('\t');

    return;

}

void FileIO::readNextLine()
{
    if(!reuse) {
        QString nextLineRaw = file->readLine();
        nextLine = nextLineRaw.split('\t');
    }
    reuse = false;

    if( nextLine.value(TIME).toDouble() <= currentSimTime )
        currentLine = nextLine;
    else
        reuse = true;
}


QString FileIO::getValue(FlightData index)
{
    return currentLine.value(index);
}

void FileIO::incrementCurrentSimTime(double step)
{
    currentSimTime += step;
}


bool FileIO::write(const QString &data)
{
    emit error("Not implemented");
    return false;
}
