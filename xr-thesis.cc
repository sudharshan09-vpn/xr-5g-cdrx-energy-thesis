#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h" 
#include "ns3/packet-sink.h" 
#include <fstream>
#include <string>
#include <vector>

// ==========================================
// 5G NR & MOBILITY HEADERS
// ==========================================
#include "ns3/nr-module.h"
#include "ns3/mobility-module.h"
#include "ns3/cc-bwp-helper.h" 

// ==========================================
// ENERGY MODEL HEADERS
// ==========================================
#include "ns3/energy-module.h"
#include "ns3/basic-energy-source-helper.h"
#include "ns3/simple-device-energy-model.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("XrThesisFinal");

std::ofstream g_energyLog; 

// ==========================================
// THE CUSTOM APPLICATION-LAYER ENERGY MONITOR
// ==========================================
void DynamicEnergyMonitor (Ptr<ns3::energy::SimpleDeviceEnergyModel> energyModel, Ptr<PacketSink> sink, uint64_t lastTotalRx, uint32_t inactivityTimer, uint32_t msSinceLastRx, uint32_t ueId)
{
  uint64_t currentTotalRx = sink->GetTotalRx ();
  double currentDraw_mA = 0.0; 
  uint32_t nextMsSinceLastRx = msSinceLastRx;
  
  if (currentTotalRx > lastTotalRx) 
    {
      energyModel->SetCurrentA (0.313); 
      currentDraw_mA = 313.0; 
      nextMsSinceLastRx = 0; 
    } 
  else 
    {
      if (msSinceLastRx < inactivityTimer) 
        {
          energyModel->SetCurrentA (0.313); 
          currentDraw_mA = 313.0;
          nextMsSinceLastRx++;
        }
      else 
        {
          energyModel->SetCurrentA (0.0114); 
          currentDraw_mA = 11.4; 
          nextMsSinceLastRx++; 
        }
    }
  
  if (g_energyLog.is_open()) 
    {
      g_energyLog << Simulator::Now().GetSeconds() << "," << ueId << "," << currentDraw_mA << "\n";
    }
  
  Simulator::Schedule (MilliSeconds (1), &DynamicEnergyMonitor, energyModel, sink, (uint64_t) currentTotalRx, inactivityTimer, (uint32_t) nextMsSinceLastRx, ueId);
}

int main (int argc, char *argv[])
{
  Time::SetResolution (Time::NS);

  // ==========================================
  // COMMAND LINE ARGUMENT PARSING
  // ==========================================
  uint32_t inactivityTimer = 2; 
  uint32_t cycleLength = 10;    
  uint32_t nUes = 20; 
  double bandwidth = 100.0;
  double frequency = 3.5e9;
  double distance = 50.0;

  ns3::CommandLine cmd;
  cmd.AddValue ("inactivityTimer", "C-DRX Inactivity Timer in ms", inactivityTimer);
  cmd.AddValue ("cycleLength", "C-DRX Cycle Length in ms", cycleLength);
  cmd.AddValue ("nUes", "Number of XR User Equipments", nUes);
  cmd.AddValue ("bandwidth", "Channel bandwidth in MHz", bandwidth);
  cmd.AddValue ("frequency", "Carrier frequency in Hz", frequency);
  cmd.AddValue ("distance", "Distance between gNB and UE in meters", distance);
  cmd.Parse (argc, argv);

  NS_LOG_UNCOND ("--------------------------------------------------");
  NS_LOG_UNCOND ("XR CAPACITY SIMULATION: DEPLOYMENT PARAMETERS");
  NS_LOG_UNCOND ("XR Headsets (Density): " << nUes);
  NS_LOG_UNCOND ("Bandwidth            : " << bandwidth << " MHz");
  NS_LOG_UNCOND ("Frequency            : " << frequency / 1e9 << " GHz");
  NS_LOG_UNCOND ("Distance             : " << distance << " m");
  NS_LOG_UNCOND ("Inactivity Timer     : " << inactivityTimer << " ms");
  NS_LOG_UNCOND ("Cycle Length         : " << cycleLength << " ms");
  NS_LOG_UNCOND ("--------------------------------------------------");

  NodeContainer gnbNodes; 
  gnbNodes.Create(1);
  
  NodeContainer ueNodes;  
  ueNodes.Create(nUes); 

  Ptr<NrPointToPointEpcHelper> epcHelper = CreateObject<NrPointToPointEpcHelper> ();
  Ptr<IdealBeamformingHelper> idealBeamformingHelper = CreateObject<IdealBeamformingHelper>();
  idealBeamformingHelper->SetAttribute ("BeamformingMethod", TypeIdValue (DirectPathBeamforming::GetTypeId ()));

  Ptr<NrHelper> nrHelper = CreateObject<NrHelper> ();
  nrHelper->SetBeamformingHelper (idealBeamformingHelper);
  nrHelper->SetEpcHelper (epcHelper);

  MobilityHelper mobility;
  mobility.SetMobilityModel ("ns3::ConstantPositionMobilityModel");
  
  Ptr<ListPositionAllocator> positionAlloc = CreateObject<ListPositionAllocator> ();
  positionAlloc->Add (Vector (0.0, 0.0, 10.0)); 
  for (uint32_t i = 0; i < ueNodes.GetN(); ++i) 
    {
      positionAlloc->Add (Vector (distance, 0.0, 1.5)); 
    }
  mobility.SetPositionAllocator (positionAlloc);
  
  mobility.Install (gnbNodes);
  mobility.Install (ueNodes);

  CcBwpCreator::SimpleOperationBandConf bandConf (frequency, bandwidth * 1e6, 1); 
  std::vector<CcBwpCreator::SimpleOperationBandConf> bandConfs { bandConf };
  auto bwps = nrHelper->CreateBandwidthParts (bandConfs, "UMa", "LOS", "ThreeGpp");
  auto allBwps = bwps.second;

  NetDeviceContainer gnbNetDev = nrHelper->InstallGnbDevice (gnbNodes, allBwps);
  NetDeviceContainer ueNetDev = nrHelper->InstallUeDevice (ueNodes, allBwps);

  InternetStackHelper stack;
  stack.Install (gnbNodes);
  stack.Install (ueNodes);
  
  Ipv4InterfaceContainer ueIpIface = epcHelper->AssignUeIpv4Address (NetDeviceContainer (ueNetDev));
  
  for (uint32_t i = 0; i < ueNodes.GetN(); ++i) 
    {
      nrHelper->AttachToGnb (ueNetDev.Get (i), gnbNetDev.Get (0));
    }

  BasicEnergySourceHelper basicSourceHelper;
  basicSourceHelper.Set("BasicEnergySourceInitialEnergyJ", DoubleValue(10000.0)); 
  auto energySources = basicSourceHelper.Install(ueNodes);
  
  std::vector<Ptr<ns3::energy::SimpleDeviceEnergyModel>> ueEnergyModels;

  for (uint32_t i = 0; i < ueNodes.GetN(); ++i) 
    {
      Ptr<ns3::energy::SimpleDeviceEnergyModel> simpleModel = CreateObject<ns3::energy::SimpleDeviceEnergyModel> ();
      simpleModel->SetNode (ueNodes.Get (i));
      simpleModel->SetEnergySource (energySources.Get (i));
      simpleModel->SetCurrentA (0.0114); 
      energySources.Get (i)->AppendDeviceEnergyModel (simpleModel);
      ueEnergyModels.push_back(simpleModel);
    }

  uint16_t port = 4477;
  
  for (uint32_t i = 0; i < ueNodes.GetN(); ++i) 
    {
      PacketSinkHelper sink ("ns3::UdpSocketFactory", InetSocketAddress (Ipv4Address::GetAny (), port));
      ApplicationContainer serverApp = sink.Install (ueNodes.Get (i));
      serverApp.Start (Seconds (0.0));
      serverApp.Stop (Seconds (10.0));

      OnOffHelper onOffHelper ("ns3::UdpSocketFactory", Address (InetSocketAddress (ueIpIface.GetAddress(i), port)));
      onOffHelper.SetAttribute ("OnTime", StringValue ("ns3::ConstantRandomVariable[Constant=0.0001]"));
      onOffHelper.SetAttribute ("OffTime", StringValue ("ns3::NormalRandomVariable[Mean=0.0166|Variance=0.0004|Bound=0.005]"));
      onOffHelper.SetAttribute ("DataRate", StringValue ("100Mbps")); 
      onOffHelper.SetAttribute ("PacketSize", UintegerValue (1024)); 

      ApplicationContainer clientApp = onOffHelper.Install (epcHelper->GetPgwNode ());
      clientApp.Start (Seconds (1.0));
      clientApp.Stop (Seconds (10.0));

      Ptr<PacketSink> ueSink = DynamicCast<PacketSink> (serverApp.Get (0));
      
      Simulator::Schedule (Seconds (1.0), &DynamicEnergyMonitor, ueEnergyModels[i], ueSink, (uint64_t) 0, inactivityTimer, (uint32_t) 0, i);
    }

  FlowMonitorHelper flowmon;
  Ptr<FlowMonitor> monitor = flowmon.InstallAll();
  
  g_energyLog.open("parsed_power_data.csv");
  g_energyLog << "Time_s,UE_ID,Current_mA\n"; 

  Simulator::Stop (Seconds (11.0)); 
  Simulator::Run ();

  if (g_energyLog.is_open()) 
    {
      g_energyLog.close();
    }

  std::string xmlName = "simulation_results/xr_latency_ues" + std::to_string(nUes) + "_timer" + std::to_string(inactivityTimer) + "_cycle" + std::to_string(cycleLength) + ".xml";
  monitor->SerializeToXmlFile(xmlName, true, true);

  Ptr<ns3::energy::BasicEnergySource> clientBattery = DynamicCast<ns3::energy::BasicEnergySource> (energySources.Get(0));
  NS_LOG_UNCOND ("[ENERGY MODEL] XR Headset 0 Remaining Energy: " << clientBattery->GetRemainingEnergy() << " Joules.");

  Simulator::Destroy ();
  return 0;
}