// Receiver.h
#ifndef __RECEIVER_H
#define __RECEIVER_H

#include <omnetpp.h>
#include "MyMessage_m.h"

using namespace omnetpp;

class Receiver : public cSimpleModule
{
  private:
    cOutVector hopCountVector;
    cStdDev    hopCountStats;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};

#endif
