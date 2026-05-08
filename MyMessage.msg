// MyMessage.msg
// OMNeT++ custom message for Hop Counting simulation

cplusplus {{
#include <string>
}}

message MyMessage
{
    int hopCount = 0;    // incremented at every router
    int ttl      = 20;   // decremented at every router; drop when 0
    int messageId = 1;   // unique packet ID
}
