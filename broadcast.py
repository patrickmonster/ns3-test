from ns import ns

from ctypes import c_int, c_float

nCsma = c_int(10)
sTime = ns.core.Seconds(100.0)
ns.core.LogComponentEnable("UdpEchoClientApplication", ns.core.LOG_LEVEL_INFO)
ns.core.LogComponentEnable("UdpEchoServerApplication", ns.core.LOG_LEVEL_INFO)

nodes = ns.network.NodeContainer()
nodes.Create(nCsma.value)




csma = ns.csma.CsmaHelper()
csma.SetChannelAttribute("DataRate", ns.core.StringValue("10Mbps"))
csma.SetChannelAttribute("Delay", ns.core.TimeValue(ns.core.NanoSeconds(6560)))

csmaDevices = csma.Install(nodes)

stack = ns.internet.InternetStackHelper()
stack.Install(nodes)

address = ns.internet.Ipv4AddressHelper()
address.SetBase(ns.network.Ipv4Address("10.1.1.0"),
                ns.network.Ipv4Mask("255.255.255.0"))

# interfaces = address.Assign(devices)
interfaces = address.Assign(csmaDevices)

echoServer = ns.applications.UdpEchoServerHelper(9)

serverApps = echoServer.Install(nodes.Get(0))
serverApps.Start(ns.core.Seconds(1.0))
serverApps.Stop(sTime)

def sendMessage(idx):
    address = ns.addressFromIpv4Address(interfaces.GetAddress(0))
    echoClient = ns.applications.UdpEchoClientHelper(address, 9)
    echoClient.SetAttribute("MaxPackets", ns.core.UintegerValue(1))
    echoClient.SetAttribute("Interval", ns.core.TimeValue(ns.core.Seconds(1.0)))
    echoClient.SetAttribute("PacketSize", ns.core.UintegerValue(1024))

    clientApps = echoClient.Install(nodes.Get(idx))
    clientApps.Start(ns.core.Seconds(2.0))
    clientApps.Stop(sTime)
for i in range(1, nCsma.value):
    sendMessage(i)



# # 출력부분
print("Tracing")
ascii = ns.AsciiTraceHelper()
csma.EnableAsciiAll(ascii.CreateFileStream("broadcast.tr"))
csma.EnablePcapAll("broadcast", False)

ns.core.Simulator.Run()
ns.core.Simulator.Destroy()