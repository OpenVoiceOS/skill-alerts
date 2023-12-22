/*
 * Copyright 2018 Aditya Mehra <aix.m@outlook.com>
 * 
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.5 as Kirigami
import org.kde.plasma.core 2.0 as PlasmaCore
import QtGraphicalEffects 1.0
import Mycroft 1.0 as Mycroft


Mycroft.Delegate {
    id: todoListView
    anchors.fill: parent
    property bool horizontalMode: root.width > root.height ? 1 : 0
    property var todoModel: sessionData.items

    Rectangle {
        color: Kirigami.Theme.backgroundColor
        anchors.fill: parent

        Rectangle {
            id: topArea
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: Kirigami.Units.gridUnit * 4
            color: Kirigami.Theme.highlightColor

            Label {
                id: listHeader
                anchors.left: parent.left
                anchors.top: parent.top
                anchors.right: parent.right
                anchors.bottom: parent.bottom
                anchors.leftMargin: Mycroft.Units.gridUnit
                text: sessionData.header
                horizontalAlignment: Text.AlignLeft
                verticalAlignment: Text.AlignVCenter
                font.pixelSize: topArea.height * 0.4
                elide: Text.ElideLeft
                maximumLineCount: 1
                color: Kirigami.Theme.textColor
            }

            Kirigami.Separator {
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: Kirigami.Units.largeSpacing
                anchors.rightMargin: Kirigami.Units.largeSpacing
                height: 1
                color: Kirigami.Theme.textColor
            }
        }

        ScrollBar {
            id: listViewScrollBar
            anchors.right: parent.right
            anchors.rightMargin: Mycroft.Units.gridUnit
            anchors.top: listArea.top
            anchors.bottom: listArea.bottom
            policy: ScrollBar.AsNeeded
        }

        ColumnLayout {
            id: listArea
            anchors.bottom: bottomArea.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: topArea.bottom
            anchors.margins: Mycroft.Units.gridUnit * 2

            Item {
                Layout.fillWidth: true
                Layout.preferredHeight: Kirigami.Units.largeSpacing
            }

            ListView {
                id: qViewL
                Layout.fillWidth: true
                Layout.fillHeight: true
                model: todoModel
                clip: true
                currentIndex: -1
                spacing: 5
                property int cellWidth: qViewL.width
                property int cellHeight: qViewL.height / 4.6

                ScrollBar.vertical: listViewScrollBar
                
                delegate: ItemDelegate {
                    width: qViewL.cellWidth
                    height: Math.max(qViewL.cellHeight, Kirigami.Units.gridUnit * 2)
                    property var card_height : height - Kirigami.Units.largeSpacing
                    
                    background: Rectangle {
                        id: delegateSttListBg
                        radius: 10
                        color: Qt.darker(Kirigami.Theme.backgroundColor, 1.5)
                        border.color: Qt.darker(Kirigami.Theme.textColor, 2.5)
                        border.width: 1
                    }

                    onClicked: {
                        Mycroft.SoundEffects.playClickedSound(Qt.resolvedUrl("sounds/clicked.wav"))
                        triggerGuiEvent("neon.alerts.converse", {
                            "main": model.main,
                            "ident": model.ident
                        })
                    }

                    onPressed: {
                        delegateSttListBg.color = Qt.rgba(Kirigami.Theme.highlightColor.r, Kirigami.Theme.highlightColor.g, Kirigami.Theme.highlightColor.b, 0.5)
                    }

                    onReleased: {
                        delegateSttListBg.color = Qt.darker(Kirigami.Theme.backgroundColor, 1.5)
                    }

                    Rectangle {
                        id: cItm
                        anchors.top: parent.top
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.topMargin: Kirigami.Units.smallSpacing
                        anchors.bottomMargin: Kirigami.Units.smallSpacing
                        anchors.rightMargin: Kirigami.Units.smallSpacing
                        anchors.leftMargin: Kirigami.Units.smallSpacing
                        height: model.secondary ? card_height / 2 : card_height
                        width: Mycroft.Units.gridUnit * 10
                        color: Kirigami.Theme.highlightColor
                        radius: 6
                        visible: true
                        enabled: true

                        Label {
                            id: cItmLabel
                            anchors.centerIn: parent
                            wrapMode: Text.WordWrap
                            anchors.margins: Kirigami.Units.smallSpacing
                            verticalAlignment: Text.AlignVCenter
                            color: Kirigami.Theme.textColor
                            font.capitalization: Font.AllUppercase
                            font.bold: true
                            text: model.main
                        }
                    }

                    Rectangle {
                        id: cItmSuff
                        anchors.right: parent.right
                        anchors.left: parent.left
                        anchors.top: cItm.bottom
                        anchors.bottomMargin: Kirigami.Units.smallSpacing
                        anchors.rightMargin: Kirigami.Units.smallSpacing
                        anchors.leftMargin: Kirigami.Units.smallSpacing
                        height: card_height / 2
                        width: Mycroft.Units.gridUnit * 10
                        color: Qt.darker(Kirigami.Theme.highlightColor, 2.5)
                        radius: 6
                        visible: model.secondary ? 1 : 0
                        enabled: model.secondary ? 1 : 0

                        Label {
                            id: cItmSuffLabel
                            anchors.centerIn: parent
                            wrapMode: Text.WordWrap
                            anchors.margins: Kirigami.Units.smallSpacing
                            verticalAlignment: Text.AlignVCenter
                            color: Kirigami.Theme.textColor
                            font.capitalization: Font.AllUppercase
                            font.bold: true
                            text: model.secondary
                        }
                    }
                }
            }
        }

        Rectangle {
            id: bottomArea
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            height: Kirigami.Units.gridUnit * 2
            color: Kirigami.Theme.highlightColor
        }
    }
} 
