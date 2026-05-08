// Router.h
#ifndef __ROUTER_H
#define __ROUTER_H

#include <omnetpp.h>
#include "MyMessage_m.h"

using namespace omnetpp;

/**
 * Router:
 *  1. Increments hopCount
 *  2. Decrements ttl  →  drops packet if ttl reaches 0
 *  3. Forwards randomly to one output gate  (seed from omnetpp.ini)
 */
class Router : public cSimpleModule
{
  private:
    int droppedCount;

  protected:
    virtual void initialize() override;
    virtual void handleMessage(cMessage *msg) override;
    virtual void finish() override;
};

#endif
