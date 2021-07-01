import frida
import sys

session = frida.get_usb_device().attach(88906)
script_string = """
if (ObjC.available)
{
    try
    {   

       
        var sessionUserName;
        var timingIdentifier;

        var receiver_dict = ObjC.classes.NSMutableDictionary.alloc().init();
        var openred_dict = ObjC.classes.NSMutableDictionary.alloc().init(); 
        var className = "CMessageMgr";
        var funcName = "- AsyncOnAddMsg:MsgWrap:";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[2]);
            console.log("AsyncOnAddMsgArg2:"+ arg2.toString());

            var obj = new ObjC.Object(args[3]);

            console.log("AsyncOnAddMsgArg3:"+ obj.toString());

            var str = obj.toString();
            type = str.split(", ");
            if(type.indexOf("type=49")!=-1){
                console.log("Successful!!");
                console.log("receiver_dict:"+ receiver_dict);
                console.log("openred_dict:"+ openred_dict);

                //call function
                //ObjC.classes.WCRedEnvelopesLogicMgr.alloc.ReceiverQueryRedEnvelopesRequest(receiver_dict);
                var WCRedEnvelopesLogicMgr = ObjC.classes.WCRedEnvelopesLogicMgr;
                my_ReceiverQueryRedEnvelopesRequest = ObjC.chooseSync(WCRedEnvelopesLogicMgr)[0];
                my_ReceiverQueryRedEnvelopesRequest["- ReceiverQueryRedEnvelopesRequest:"](receiver_dict);
                
               // var friendlyObjc_getClass = new NativeFunction(Module.findExportByName('WeChat','objc_getClass'),'pointer',['pointer']);
                //var chunk = Memory.alloc(22);
                //console.log(chunk);
                //Memory.writeUtf8String(chunk, "WCRedEnvelopesLogicMgr");
                //console.log(Memory.readUtf8String(chunk,22));
                //var p = Memory.alloc(Process.pointerSize);

                //Memory.writeUInt(p, 0);

                //var Class = friendlyObjc_getClass(Memory.writeUtf8String(chunk, "WCRedEnvelopesLogicMgr"),p);

                //var getService = ObjC.classes.MMServiceCenter.alloc().init();
                //getService["- getService:"](Class);


                //var ReceiverQueryRedEnvelopesRequest = ObjC.classes.WCRedEnvelopesLogicMgr.alloc().init();
                //ReceiverQueryRedEnvelopesRequest["- ReceiverQueryRedEnvelopesRequest:"](receiver_dict);

                //if(timingIdentifier!=null){
                //    console.log("OpenRed");
                //    var OpenRedEnvelopesRequest = ObjC.classes.WCRedEnvelopesLogicMgr.alloc().init();
                //    OpenRedEnvelopesRequest["- OpenRedEnvelopesRequest:"](openred_dict);

                //};
                

            };

    
          },
          onLeave: function(retval) {
            string_value = ObjC.classes.NSString.stringWithString_(retval);
            console.log("Mgrretval:"+string_value+" type:"+typeof string_value);
          }
        });

        var arr;
        var url;
        var originalUrl
        var className = "WCPayInfoItem";
        var funcName = "- setM_c2cNativeUrl:";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[2]);
            //console.log("setM_c2cNativeUrl:"+ arg2.toString());
            originalUrl = arg2.toString();
            url = arg2.toString();
            var num=url.indexOf("?")
            url=url.substr(num+1); //取得所有参数   

            arr=url.split("&"); //各个参数放到数组里
            //console.log(arr);
            for(var i=0;i < arr.length;i++){
                num=arr[i].indexOf("="); //num=7,9,6,12,3,4
                
                if(num>0){
                    name=arr[i].substring(0,num);
                    value=arr[i].substr(num+1);
                    this[name]=value;
                }
                
           };
           
           //构建NSDictionary            
           
           receiver_dict.setObject_forKey_(0,"agreeDuty");
           receiver_dict.setObject_forKey_(1,"inWay");
           receiver_dict.setObject_forKey_(this["channelid"],"channelId");
           receiver_dict.setObject_forKey_(this["msgtype"],"msgType");
           receiver_dict.setObject_forKey_(originalUrl,"nativeUrl");
           receiver_dict.setObject_forKey_(this["sendid"],"sendId");
           openred_dict.setObject_forKey_("http://wx.qlogo.cn/mmhead/ver_1/kX412icQKOgUFJOWYveibyOdF9WadbrJOFnwKzxJuwXvFxiabpK4VkicujlZ9G2CXiboqOLSkZaiaGEtblCKZBHRSpbIkfc1piaAAKib4qKOic1GpdMw/132","headImg");
           openred_dict.setObject_forKey_("xiaokang","nickName");
           openred_dict.setObject_forKey_(originalUrl,"nativeUrl");
           openred_dict.setObject_forKey_(this["channelid"],"channelId");
           openred_dict.setObject_forKey_(this["msgtype"],"msgType");
           openred_dict.setObject_forKey_(this["sendid"],"sendId");
           openred_dict.setObject_forKey_(this["sendusername"],"sessionUserName");
           
            

    
          },
          onLeave: function(retval) {
            console.log("Finished!");
          }
        });



        var className = "WCRedEnvelopesLogicMgr";
        var funcName = "- OnWCToHongbaoCommonResponse:Request:";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[2]);

            //NSData转换为NSString
            console.log("OnWCToHongbaoCommonResponse:"+ Memory.readUtf8String(arg2.retText().buffer().bytes(),arg2.retText().buffer().length()));

            //将json字符串转换成json对象
            var obj = JSON.parse(Memory.readUtf8String(arg2.retText().buffer().bytes(),arg2.retText().buffer().length()));
            console.log(obj.timingIdentifier);
            timingIdentifier = obj.timingIdentifier;
            openred_dict.setObject_forKey_(timingIdentifier,"timingIdentifier");


            
            
            
          },
          onLeave: function(retval) {
            console.log("Finished!");
          }
        });

        var className = "WCRedEnvelopesLogicMgr";
        var funcName = "- ReceiverQueryRedEnvelopesRequest:";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[2]);
            console.log("ReceiverQueryRedEnvelopesRequest:"+ arg2.toString());

            
          },
          onLeave: function(retval) {
            console.log("Finished!");
          }
        });

        var className = "WCRedEnvelopesReceiveHomeView";
        var funcName = "- OnOpenRedEnvelopes";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[0]);
            console.log("OnOpenRedEnvelopes:"+ arg2.$ivars.m_dicBaseInfo);

            
          },
          onLeave: function(retval) {
            console.log("Finished!");
          }
        });

        var className = "WCRedEnvelopesLogicMgr";
        var funcName = "- OpenRedEnvelopesRequest:";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg2 = new ObjC.Object(args[2]);
            console.log("OpenRedEnvelopesRequest:"+ arg2.toString());

            
          },
          onLeave: function(retval) {
            console.log("Finished!");
          }
        });


    }
    catch(err)
    {
        console.log("[!] Exception2: " + err.message);
    }
}
else
{
    console.log("Objective-C Runtime is not available!");
}
"""


script = session.create_script(script_string)


def on_message(message, data):
    if message['type'] == 'error':
        print("[!] " + message['stack'])
    elif message['type'] == 'send':
        print("[i] " + message['payload'])
    else:
        print(message)


script.on('message', on_message)
script.load()
sys.stdin.read()












