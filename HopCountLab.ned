// HopCountNet.ned
// Mesh network: 1 Sender + 10 Routers (r0-r9) + 1 Receiver

simple Sender
{
    parameters:
        int numPackets = default(50);
    gates:
        output out;
}

simple Receiver
{
    gates:
        input in[];
}

simple Router
{
    gates:
        input  in[];
        output out[];
}

network HopCountNet
{
    submodules:
        sender   : Sender;
        receiver : Receiver;
        r0  : Router;
        r1  : Router;
        r2  : Router;
        r3  : Router;
        r4  : Router;
        r5  : Router;
        r6  : Router;
        r7  : Router;
        r8  : Router;
        r9  : Router;

    connections:

        // Sender -> R0
        sender.out      --> r0.in++;

        // R0 -> R1, R2, R3
        r0.out++ --> r1.in++;
        r0.out++ --> r2.in++;
        r0.out++ --> r3.in++;

        // R1 -> R4, R5, R2
        r1.out++ --> r4.in++;
        r1.out++ --> r5.in++;
        r1.out++ --> r2.in++;

        // R2 -> R4, R6, R5
        r2.out++ --> r4.in++;
        r2.out++ --> r6.in++;
        r2.out++ --> r5.in++;

        // R3 -> R5, R7, R6
        r3.out++ --> r5.in++;
        r3.out++ --> r7.in++;
        r3.out++ --> r6.in++;

        // R4 -> R6, R8, R7
        r4.out++ --> r6.in++;
        r4.out++ --> r8.in++;
        r4.out++ --> r7.in++;

        // R5 -> R7, R8, R9
        r5.out++ --> r7.in++;
        r5.out++ --> r8.in++;
        r5.out++ --> r9.in++;

        // R6 -> R8, R9
        r6.out++ --> r8.in++;
        r6.out++ --> r9.in++;

        // R7 -> R9, R8
        r7.out++ --> r9.in++;
        r7.out++ --> r8.in++;

        // R8 -> R9
        r8.out++ --> r9.in++;

        // R9 -> Receiver, R6, R7
        r9.out++ --> receiver.in++;
        r9.out++ --> r6.in++;
        r9.out++ --> r7.in++;
}
