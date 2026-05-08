// Sender.h
#ifndef __SENDER_H
#define __SENDER_H

#include <omnetpp.h>
#include "MyMessage_m.h"

using namespace omnetpp;

class Sender : public cSimpleModule
{
  private:
    int totalPackets;
    int sentCount;
    cMessage *sendTimer;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};

#endif
