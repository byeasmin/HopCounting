// Receiver.cc
#include "Receiver.h"

Define_Module(Receiver);

void Receiver::initialize()
{
    hopCountVector.setName("hopCount");
    hopCountStats.setName("hopCountStats");
}

void Receiver::handleMessage(cMessage *msg)
{
    MyMessage *pkt = check_and_cast<MyMessage *>(msg);

    int hops = pkt->getHopCount();
    int ttl  = pkt->getTtl();

    EV << "=== [Receiver] Packet ARRIVED ==="
       << "  finalHopCount=" << hops
       << "  remainingTTL=" << ttl
       << "\n";

    hopCountVector.record(hops);
    hopCountStats.collect(hops);
    recordScalar("finalHopCount", hops);

    delete pkt;
}

void Receiver::finish()
{
    EV << "\n=== [Receiver] FINAL STATISTICS ===\n";
    EV << "  Packets received : " << hopCountStats.getCount()  << "\n";
    EV << "  Average hop count: " << hopCountStats.getMean()   << "\n";
    EV << "  Min hop count    : " << hopCountStats.getMin()    << "\n";
    EV << "  Max hop count    : " << hopCountStats.getMax()    << "\n";
    EV << "  Std deviation    : " << hopCountStats.getStddev() << "\n";

    hopCountStats.recordAs("hopCount");
}
