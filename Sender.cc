// Sender.cc
// Sends 50 packets one by one with a small interval between each.

#include "Sender.h"

Define_Module(Sender);

void Sender::initialize()
{
    totalPackets = par("numPackets");   // read from omnetpp.ini
    sentCount    = 0;

    // Schedule the first send immediately
    sendTimer = new cMessage("sendTimer");
    scheduleAt(simTime(), sendTimer);
}

void Sender::handleMessage(cMessage *msg)
{
    if (msg == sendTimer)
    {
        if (sentCount < totalPackets)
        {
            sentCount++;

            MyMessage *pkt = new MyMessage("DataPacket");
            pkt->setHopCount(0);
            pkt->setTtl(20);
            pkt->setMessageId(sentCount);

            EV << "[Sender] Sending packet #" << sentCount
               << "  hopCount=0  ttl=20\n";

            send(pkt, "out");

            // Schedule next packet after 0.1s interval
            scheduleAt(simTime() + 0.1, sendTimer);
        }
        else
        {
            EV << "[Sender] All " << totalPackets << " packets sent.\n";
            delete sendTimer;
            sendTimer = nullptr;
        }
    }
    else
    {
        delete msg;
    }
}

void Sender::finish()
{
    EV << "[Sender] Total packets sent: " << sentCount << "\n";
}
