# WeChatHook
This script can auto open Red-Packet and modify StepCounts
Tools:Frida
Tutorials:
  1.install python3.X
  2.pip install frida-tools
  3.The phone is connected to the computer via USB(Root or Jailbreak)
  4.move frida-server to /data/local/tmp/ (Android),install frida by Cydia (IOS)
  5.open WeChat and run script
Issue:
  ‘id logicMgr = [[objc_getClass("MMServiceCenter") defaultCenter] getService:objc_getClass("WCRedEnvelopesLogicMgr")];‘
  
  I don't have a way to implement the OC code above with Frida yet,so that means the script is not really automately
  If you have any idear to implement this code and please commit it,thank you!!!
