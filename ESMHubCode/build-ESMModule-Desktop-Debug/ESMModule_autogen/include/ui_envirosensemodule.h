/********************************************************************************
** Form generated from reading UI file 'envirosensemodule.ui'
**
** Created by: Qt User Interface Compiler version 5.9.7
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_ENVIROSENSEMODULE_H
#define UI_ENVIROSENSEMODULE_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenu>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QTabWidget>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_envirosensemodule
{
public:
    QWidget *centralwidget;
    QTabWidget *MainWidget;
    QWidget *Pressure;
    QWidget *Humidity;
    QWidget *Temperature;
    QMenuBar *menubar;
    QMenu *menuESMHub;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *envirosensemodule)
    {
        if (envirosensemodule->objectName().isEmpty())
            envirosensemodule->setObjectName(QStringLiteral("envirosensemodule"));
        envirosensemodule->resize(800, 600);
        centralwidget = new QWidget(envirosensemodule);
        centralwidget->setObjectName(QStringLiteral("centralwidget"));
        MainWidget = new QTabWidget(centralwidget);
        MainWidget->setObjectName(QStringLiteral("MainWidget"));
        MainWidget->setGeometry(QRect(10, 0, 781, 421));
        Pressure = new QWidget();
        Pressure->setObjectName(QStringLiteral("Pressure"));
        MainWidget->addTab(Pressure, QString());
        Humidity = new QWidget();
        Humidity->setObjectName(QStringLiteral("Humidity"));
        MainWidget->addTab(Humidity, QString());
        Temperature = new QWidget();
        Temperature->setObjectName(QStringLiteral("Temperature"));
        MainWidget->addTab(Temperature, QString());
        envirosensemodule->setCentralWidget(centralwidget);
        menubar = new QMenuBar(envirosensemodule);
        menubar->setObjectName(QStringLiteral("menubar"));
        menubar->setGeometry(QRect(0, 0, 800, 21));
        menuESMHub = new QMenu(menubar);
        menuESMHub->setObjectName(QStringLiteral("menuESMHub"));
        envirosensemodule->setMenuBar(menubar);
        statusbar = new QStatusBar(envirosensemodule);
        statusbar->setObjectName(QStringLiteral("statusbar"));
        envirosensemodule->setStatusBar(statusbar);

        menubar->addAction(menuESMHub->menuAction());

        retranslateUi(envirosensemodule);

        MainWidget->setCurrentIndex(0);


        QMetaObject::connectSlotsByName(envirosensemodule);
    } // setupUi

    void retranslateUi(QMainWindow *envirosensemodule)
    {
        envirosensemodule->setWindowTitle(QApplication::translate("envirosensemodule", "envirosensemodule", Q_NULLPTR));
        MainWidget->setTabText(MainWidget->indexOf(Pressure), QApplication::translate("envirosensemodule", "Pressure", Q_NULLPTR));
        MainWidget->setTabText(MainWidget->indexOf(Humidity), QApplication::translate("envirosensemodule", "Humidity", Q_NULLPTR));
        MainWidget->setTabText(MainWidget->indexOf(Temperature), QApplication::translate("envirosensemodule", "Temperature", Q_NULLPTR));
        menuESMHub->setTitle(QApplication::translate("envirosensemodule", "ESMHub", Q_NULLPTR));
    } // retranslateUi

};

namespace Ui {
    class envirosensemodule: public Ui_envirosensemodule {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_ENVIROSENSEMODULE_H
