from ns import ns
import sys
from ctypes import c_int, c_bool, c_char_p, create_string_buffer

Plot = c_bool(True)
nCsma = c_int(30)
packet_i = ns.core.UintegerValue(50000)
sTime = ns.core.Seconds(100.0)
ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)
# ns.core.GlobalValue.Bind("ChecksumEnabled", ns.core.BooleanValue(True))
# ns.core.GlobalValue.Bind("PcapFile", ns.core.StringValue("udp-echo.pcap"))


BUFFLEN = 8192
ResultsBuffer = create_string_buffer(b"output1.xml", BUFFLEN)
Results = c_char_p(ResultsBuffer.raw)

nodes = ns.network.NodeContainer()
nodes.Create(nCsma.value)


point_to_point = ns.network.PointToPointHelper()
point_to_point.SetDeviceAttribute("DataRate", ns.core.StringValue("50Kbps"))
point_to_point.SetChannelAttribute("Delay", ns.core.StringValue("1ms"))

# csma = ns.csma.CsmaHelper()
# csma.SetChannelAttribute("DataRate", ns.core.StringValue("50Kbps"))
# csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(1)))


devices = []
for i in range(0,nCsma.value) :
    for j in range(i + 1, nCsma.value) :
        device = point_to_point.Install(nodes.Get(i), nodes.Get(j))
        devices.append(device)

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

# Configure IPv4 address for each network node
ipv4 = ns.internet.Ipv4AddressHelper()
ipv4.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))


addresses = [] # 인터페이스 집합
for i in range(nCsma.value):
    address = ipv4.Assign(ns.network.NetDeviceContainer(devices[i]))
    addresses.append(address)

def createServer (idx, port) :
    echoServer = ns.applications.UdpEchoServerHelper(port)

    serverApps = echoServer.Install(nodes.Get(idx))
    serverApps.Start(ns.core.Seconds(1.0))
    serverApps.Stop(sTime)

# address = ns.addressFromIpv4Address(interfaces.GetAddress(0))


address = ns.addressFromIpv4Address(ns.network.Ipv4Address.GetBroadcast())
# address = ns.addressFromIpv4Address(addresses[0].GetAddress(0))
# broadcast_address = ns.network.InetSocketAddress(ns.network.Ipv4Address.GetBroadcast(), 9)

echoClient = ns.applications.UdpEchoClientHelper(address, 9)
echoClient.SetAttribute("MaxPackets", packet_i)
echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(3)))
echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(100))


createServer(0, 9)
# Create and schedule events for the start and stop time
for i in range(1,nCsma.value):
    echoClient.Install(nodes.Get(i))
    createServer(i, 9)

# for i in range(1, nCsma.value) : 
#     sendMessage(i, interfaces.GetAddress(0), 9)


flowmon_helper = ns.flow_monitor.FlowMonitorHelper();

flowmon_helper.InstallAll()
monitor = flowmon_helper.GetMonitor()
monitor.SetAttribute("DelayBinWidth", ns.core.DoubleValue(0.001))
monitor.SetAttribute("JitterBinWidth", ns.core.DoubleValue(0.001))
monitor.SetAttribute("PacketSizeBinWidth", ns.core.DoubleValue(20))

# Start the simulation and run until the stop time
# ns.core.Simulator.Run(stop_time)

# Clean up the simulation
# ns.core.Simulator.Destroy()

# ns.internet.Ipv4GlobalRoutingHelper.PopulateRoutingTables()

#  interfaces.GetAddress(0) / ns.Ipv4Address.GetBroadcast()
# def sendMessage(idx, addr, port):
#     address = ns.addressFromIpv4Address(addr)
#     echoClient = ns.applications.UdpEchoClientHelper(address, port)
#     echoClient.SetAttribute("MaxPackets", packet_i)
#     echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(3)))
#     echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(200))

#     clientApps = echoClient.Install(nodes.Get(idx))
#     clientApps.Start(ns.core.Seconds(.1))
#     clientApps.Stop(sTime)

# # 라우팅 테이블 구성

# createServer(0, 9)
# # 브로드 캐스팅
# for i in range(1, nCsma.value):
#     createServer(i, 9)
#     # for j in range(1, nCsma.value):       
#     sendMessage(i, ns.Ipv4Address.GetBroadcast(), 9)


# # # 출력부분
# print("Tracing")
# # ascii = ns.AsciiTraceHelper()
# # csma.EnableAsciiAll(ascii.CreateFileStream("broadcast.tr"))
# # csma.EnablePcapAll("broadcast", False)

# flowmon_helper = ns.flow_monitor.FlowMonitorHelper();

# flowmon_helper.InstallAll()
# monitor = flowmon_helper.GetMonitor()
# monitor.SetAttribute("DelayBinWidth", ns.core.DoubleValue(0.001))
# monitor.SetAttribute("JitterBinWidth", ns.core.DoubleValue(0.001))
# monitor.SetAttribute("PacketSizeBinWidth", ns.core.DoubleValue(20))

ns.core.Simulator.Stop(sTime)
ns.core.Simulator.Run()
# ns.core.Simulator.Destroy()

# exit()
# 

def print_stats(os, st):
    print ("  Tx Bytes: ", st.txBytes, file=os)
    print ("  Rx Bytes: ", st.rxBytes, file=os)
    print ("  Tx Packets: ", st.txPackets, file=os)
    print ("  Rx Packets: ", st.rxPackets, file=os)
    print ("  Lost Packets: ", st.lostPackets, file=os)
    # if st.rxPackets > 0:
    #     print ("  Mean{Delay}: ", (st.delaySum.GetSeconds() / st.rxPackets), file=os)
    #     print ("  Mean{Jitter}: ", (st.jitterSum.GetSeconds() / (st.rxPackets-1)), file=os)
    #     print ("  Mean{Hop Count}: ", float(st.timesForwarded) / st.rxPackets + 1, file=os)

    if 0:
        print ("Delay Histogram", file=os)
        for i in range(st.delayHistogram.GetNBins () ):
            print (" ",i,"(", st.delayHistogram.GetBinStart (i), "-", \
                st.delayHistogram.GetBinEnd (i), "): ", st.delayHistogram.GetBinCount (i), file=os)
        print ("Jitter Histogram", file=os)
        for i in range(st.jitterHistogram.GetNBins () ):
            print (" ",i,"(", st.jitterHistogram.GetBinStart (i), "-", \
                st.jitterHistogram.GetBinEnd (i), "): ", st.jitterHistogram.GetBinCount (i), file=os)
        print ("PacketSize Histogram", file=os)
        for i in range(st.packetSizeHistogram.GetNBins () ):
            print (" ",i,"(", st.packetSizeHistogram.GetBinStart (i), "-", \
                st.packetSizeHistogram.GetBinEnd (i), "): ", st.packetSizeHistogram.GetBinCount (i), file=os)

    for reason, drops in enumerate(st.packetsDropped):
        print ("  Packets dropped by reason %i: %i" % (reason, drops), file=os)
    #for reason, drops in enumerate(st.bytesDropped):
    #    print "Bytes dropped by reason %i: %i" % (reason, drops)

monitor.CheckForLostPackets()
classifier = flowmon_helper.GetClassifier()

if Results.value != b"output.xml":
    for flow_id, flow_stats in monitor.GetFlowStats():
        t = classifier.FindFlow(flow_id)
        proto = {6: 'TCP', 17: 'UDP'} [t.protocol]
        print ("FlowID: %i (%s %s/%s --> %s/%i)" % \
            (flow_id, proto, t.sourceAddress, t.sourcePort, t.destinationAddress, t.destinationPort))
        print_stats(sys.stdout, flow_stats)
else:
    res = monitor.SerializeToXmlFile(Results.value.decode("utf-8"), True, True)
    print (res)


if Plot.value:
    import pylab
    delays = []
    tx = [] # 발신
    rx = [] # 수신
    lostPackets = [] # 수신
    for flow_id, flow_stats in monitor.GetFlowStats():
        tupl = classifier.FindFlow(flow_id)
        print(tupl)
        # if flow_id != 0: continue
        # if tupl.sourcePort != 9 : continue
        # if tupl.sourceAddress != 9 : continue
        # if tupl.protocol == 17 : continue
        tx.append(flow_stats.txPackets)
        rx.append(flow_stats.rxPackets)
        lostPackets.append(flow_stats.lostPackets)
        # print(flow_stats.rxPackets)
        # delays.append(flow_stats.delaySum.GetSeconds() / flow_stats.rxPackets)
        # if ( flow_stats.rxPackets) : 
        #     delays.append(flow_stats.delaySum.GetSeconds() / flow_stats.rxPackets)
        # else :
        #     delays.append(0)
    # pylab.plot(delays)
    pylab.plot(tx, label = "Tx", color="dodgerblue")
    pylab.plot(rx, label = "Rx", color="red")
    pylab.plot(lostPackets, label = "Lost Packets")
    # pylab.plot(lostPackets, label = "Rx", color="dodgerblue")
    # pylab.plot(rx, label = "Lost Packets", color="red")

    # 범위
    pylab.axis([-1,30, -1, 40])

    pylab.xlabel("Delay (s)")
    pylab.ylabel("Tx")
    pylab.legend(loc="lower left")
    pylab.show()