#include <QtGui/QGuiApplication>
#include "qtquick2applicationviewer.h"

#include <QSurface>
#include <QSurfaceFormat>
#include <QDebug>

#include <QQmlApplicationEngine>
#include <QQmlComponent>

#include "fileio.h"

int main(int argc, char *argv[])
{
    QGuiApplication app(argc, argv);

    QtQuick2ApplicationViewer viewer;

    FileIO::declareQML();

    /* Make Background Transparent */
    viewer.setColor(QColor(Qt::transparent));
    viewer.setClearBeforeRendering(true);

    viewer.setMainQmlFile(QStringLiteral("qml/QtOSD/main.qml"));
    viewer.showExpanded();

    return app.exec();
}
