from ns import ns
import sys

cmd = ns.core.CommandLine()
cmd.Parse(sys.argv)

# # Create 10 nodes
nodes = ns.network.NodeContainer()
nodes.Create(17)


# Read node connections from a text file

p2p = ns.network.PointToPointHelper()
p2p.SetDeviceAttribute("DataRate", ns.core.DataRateValue(10000000))
p2p.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.MilliSeconds(2)))


devices = ns.network.NetDeviceContainer()
with open("./isls.txt", 'r') as o:
    for line in o.readlines():
        a, b = line.strip().split(" ");
        devices.Add(p2p.Install(nodes.Get(a), nodes.Get(b)))


# Install UDP broadcast application on all nodes
broadcast_helper = ns.applications.UdpBroadcastHelper(17)
broadcast_apps = broadcast_helper.Install(nodes)


# Set the start and stop time for the simulation
start_time = ns.core.Seconds(0.0)
stop_time = ns.core.Seconds(10.0)


# Create and schedule events for the start and stop time
start_event = ns.core.Simulator.Schedule(start_time, ns.core.MakeEventSource("ns3::StartApplication", "Application", broadcast_apps))
stop_event = ns.core.Simulator.Schedule(stop_time, ns.core.MakeEventSource("ns3::StopApplication", "Application", broadcast_apps))

# # 출력부분
print("Tracing")
ascii = ns.AsciiTraceHelper()
p2p.EnableAsciiAll(ascii.CreateFileStream("broadcast.tr"))
p2p.EnablePcapAll("broadcast", False)


# Start the simulation and run until the stop time
ns.core.Simulator.Run(stop_time)
ns.core.Simulator.Destroy()

# # Install internet stack on the nodes
# stack = ns.internet.InternetStackHelper()
# stack.Install(nodes)

# # Assign IPv4 addresses to the net devices
# address = ns.internet.Ipv4AddressHelper()
# address.SetBase(ns.network.Ipv4Address("10.1.1.0"), ns.network.Ipv4Mask("255.255.255.0"))
# interfaces = address.Assign(devices)


# port = 50000

# localAddress = ns.network.InetSocketAddress(interfaces.GetAddress(1), port)
# packetSinkHelper = ns.applications.PacketSinkHelper("ns3::TcpSocketFactory", localAddress)
# sinkApps = packetSinkHelper.Install(nodes.Get(1))
# sinkApps.Start(ns.core.Seconds(0.0))
# sinkApps.Stop(ns.core.Seconds(10.0))


# # Broadcast SYN packet from the first node
# broadcastAddress = ns.network.AddressValue(ns.network.InetSocketAddress(ns.network.Ipv4Address.GetBroadcast(), port))
# onoffHelper = ns.applications.OnOffHelper("ns3::TcpSocketFactory", broadcastAddress)
# onoffHelper.SetAttribute("DataRate", ns.core.StringValue("5Mbps"))
# onoffHelper.SetAttribute("PacketSize", ns.core.UintegerValue(1500))
# onoffHelper.SetAttribute("OnTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=1.0]"))
# onoffHelper.SetAttribute("OffTime", ns.core.StringValue("ns3::ConstantRandomVariable[Constant=0.0]"))
# apps = onoffHelper.Install(nodes.Get(0))
# apps.Start(ns.core.Seconds(0.0))
# apps.Stop(ns.core.Seconds(10.0))

# # Configure TCP flow scheduler
# classifier = ns.tcp_flow.TcpFlowClassifier()
# classifier.SetProtocol(ns.tcp.TcpHeader.SYN)

# scheduler = ns.tcp_flow.TcpFlowScheduler()
# scheduler.SetClassifier(classifier)

# flow_helper = ns.tcp_flow.TcpFlowSendHelper()
# flow_helper.SetSocketType("ns3::TcpSocketFactory")
# flow_helper.SetRemoteAddress(broadcastAddress)
# flow_helper.SetLocalAddress(interfaces.GetAddress(0))
# flow_helper.SetRemotePort(port)

# header = ns.tcp.TcpHeader()
# header.SetFlags(ns.tcp.TcpHeader.SYN)
# header.SetSourcePort(port)
# header.SetDestinationPort(port)
# header.SetSequenceNumber(1)
# header.SetWindowSize(65535)

# flow_helper.SetHeader(header)
# flow_helper.Initialize()
# flow_helper.Start(ns.core.Seconds(0.0))

# ns.core.Simulator.Run()
# ns.core.Simulator.Destroy()