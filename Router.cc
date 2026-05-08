// Router.cc

#include "Router.h"

Define_Module(Router);

void Router::initialize()
{
    droppedCount = 0;
}

void Router::handleMessage(cMessage *msg)
{
    MyMessage *pkt = check_and_cast<MyMessage *>(msg);

    // ── Step 1: Increment hop count ──────────────────────────────────────
    pkt->setHopCount(pkt->getHopCount() + 1);

    // ── Step 2: Decrement TTL ────────────────────────────────────────────
    pkt->setTtl(pkt->getTtl() - 1);

    EV << "[" << getName() << "]"
       << "  hopCount=" << pkt->getHopCount()
       << "  ttl="      << pkt->getTtl()
       << "\n";

    // ── Step 3: Drop if TTL expired ──────────────────────────────────────
    if (pkt->getTtl() <= 0) {
        EV << "[" << getName() << "] TTL=0 → DROPPING packet at hopCount="
           << pkt->getHopCount() << "\n";
        droppedCount++;
        delete pkt;
        return;
    }

    // ── Step 4: Random forwarding ────────────────────────────────────────
    int numOut = gateSize("out");
    if (numOut == 0) {
        EV << "[" << getName() << "] No output gates → dropping.\n";
        droppedCount++;
        delete pkt;
        return;
    }

    int chosen = intuniform(0, numOut - 1);   // uniform random gate
    EV << "[" << getName() << "] Forwarding on gate out[" << chosen << "]\n";
    send(pkt, "out", chosen);
}

void Router::finish()
{
    recordScalar("droppedPackets", droppedCount);
    EV << "[" << getName() << "] Packets dropped (TTL): " << droppedCount << "\n";
}
