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
                var friendlyObjc_getClass = new NativeFunction(Module.findExportByName('WeChat','objc_getClass'),'pointer',['pointer']);
                var chunk = Memory.alloc(22);
                //console.log(chunk);
                Memory.writeUtf8String(chunk, "WCRedEnvelopesLogicMgr");
                console.log(Memory.readUtf8String(chunk,22));
                var p = Memory.alloc(Process.pointerSize);

                Memory.writeUInt(p, 0);

                var Class = friendlyObjc_getClass(Memory.writeUtf8String(chunk, "WCRedEnvelopesLogicMgr"),p);

                var getService = ObjC.classes.MMServiceCenter.alloc().init();
                getService["- getService:"](Class);


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



# if(type.indexOf("type=49")!=-1){
#                 console.log("Successful!!");
#                 //console.log("sendId:" + sendId);

#                 var my_obj=ObjC.classes.WCRedEnvelopesLogicMgr.alloc().init();
#                 my_obj["- ReceiverQueryRedEnvelopesRequest:"](ns_dict);

#                 //构建NSDictionary
                
#                 ns_dict.setObject_forKey_("http://wx.qlogo.cn/mmhead/ver_1/kX412icQKOgUFJOWYveibyOdF9WadbrJOFnwKzxJuwXvFxiabpK4VkicujlZ9G2CXiboqOLSkZaiaGEtblCKZBHRSpbIkfc1piaAAKib4qKOic1GpdMw/132","headImg");
#                 ns_dict.setObject_forKey_("xiaokang","nickName");
#                 ns_dict.setObject_forKey_(sessionUserName,"sessionUserName");
#                 ns_dict.setObject_forKey_(timingIdentifier,"timingIdentifier");
#                 console.log(ns_dict);
#                 //console.log(ns_dict.objectForKey_('channelId'));

#                 //call function
#                 var my_obj=ObjC.classes.WCRedEnvelopesLogicMgr.alloc().init();
#                 my_obj["- OpenRedEnvelopesRequest:"](ns_dict);



#             };


# 红包参数:
# [<WCRedEnvelopesLogicMgr: 0x171030740> OpenRedEnvelopesRequest:{
#     channelId = 1;
#     headImg = "http://wx.qlogo.cn/mmhead/ver_1/kX412icQKOgUFJOWYveibyOdF9WadbrJOFnwKzxJuwXvFxiabpK4VkicujlZ9G2CXiboqOLSkZaiaGEtblCKZBHRSpbIkfc1piaAAKib4qKOic1GpdMw/132";
#     msgType = 1;
#     nativeUrl = "wxpay://c2cbizmessagehandler/hongbao/receivehongbao?msgtype=1&channelid=1&sendid=1000039401201810227014413563162&sendusername=haomeng521wanghui&ver=6&sign=86152cf1cb3a028bcaeb5fd1197f752af59f78a4593e212763b96242ed2a274fad8f5a781fefa02268ea1684f30cd0fc8461c67835dba9b0b0550d436cea9544805ea39be753b59da4dd030a58d2b1fe";
#     nickName = "\U5c0f\U5eb7";
#     sendId = 1000039401201810227014413563162;
#     sessionUserName = haomeng521wanghui;
#     timingIdentifier = D306A5E26578A1543882AA1D95541ECF;
# } ]

# receiver_dict
# Request:{
#     agreeDuty = 0;
#     channelId = 1;
#     inWay = 1;
#     msgType = 1;
#     nativeUrl = "wxpay://c2cbizmessagehandler/hongbao/receivehongbao?msgtype=1&channelid=1&sendid=1000039501201811057003301209049&sendusername=haomeng521wanghui&ver=6&sign=ccd6e18bba171be2420a349ec080b51e16a004b66e189a791c7f0ebe68d297239e94d33d2de91670ee84bf06ef9a64f78cfad261b03c83a5d205ec08ae9280528cf2a6a68679021bb3e9e440ca4d450c";
#     sendId = 1000039501201811057003301209049;
# }

# openred_dict
# RedEnve:{
#     channelId = 1;
#     headImg = "http://wx.qlogo.cn/mmhead/ver_1/PJojDcMy7pKy4Xbj8GrEuofassaFptzjeBx6Y3OffcGtyicn1wUkZ8iagKheW9S6dKSqA6ue8eE8zyG5kPxQwjrS1OpTVPW3f1lHF0wGnuia2c/132";
#     msgType = 1;
#     nativeUrl = "wxpay://c2cbizmessagehandler/hongbao/receivehongbao?msgtype=1&channelid=1&sendid=1000039501201811057003301209049&sendusername=haomeng521wanghui&ver=6&sign=ccd6e18bba171be2420a349ec080b51e16a004b66e189a791c7f0ebe68d297239e94d33d2de91670ee84bf06ef9a64f78cfad261b03c83a5d205ec08ae9280528cf2a6a68679021bb3e9e440ca4d450c";
#     nickName = xiaokang;
#     sendId = 1000039501201811057003301209049;
#     sessionUserName = haomeng521wanghui;
#     timingIdentifier = 2B661EA9651588D9D568243216927B62;
# }



#hook function
# var className = "CMessageWrap";
# var funcName = "- m_uiMessageType";
# var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
# console.log("[*] Class Name: " + className);
# console.log("[*] Method Name: " + funcName);
# Interceptor.attach(hook.implementation, {
#   onEnter: function(args) {
#     var obj = new ObjC.Object(args[0]);
#     console.log("Wrapargs:"+ obj.toString());
    
#   },
#   onLeave: function(retval) {
#     console.log("Wrapretval:"+retval+" type:"+typeof retval);
    
#   }
# });


# var className = "WCRedEnvelopesLogicMgr";
# var funcName = "- OpenRedEnvelopesRequest:";
# var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
# console.log("[*] Class Name: " + className);
# console.log("[*] Method Name: " + funcName);
# Interceptor.attach(hook.implementation, {
#   onEnter: function(args) {
#     console.log("Redparam:"+args[2]+" type:"+typeof args[2]);

#   },
#   onLeave: function(retval) {
#     console.log("Redpretval:"+retval+" type:"+typeof retval);
    
#   }
# });

#//js dictionary
# function Dictionary() {
#     var items = {};

#     this.has = function (key) {
#         return key in items;
#     };

#     this.set = function (key, value) {
#         items[key] = value;
#     };

#     this.remove = function (key) {
#         if (this.has(key)) {
#             delete items[key];
#             return true;
#         }
#         return false;
#     };

#     this.get = function (key) {
#         return this.has(key) ? items[key] : undefined;
#     };

#     this.values = function () {
#         var values = [];
#         for (var k in items) {
#             if (this.has(k)) {
#                 values.push(items[k]);
#             }
#         }
#         return values;
#     };

#     this.clear = function () {
#         items = {};
#     };

#     this.size = function () {
#         var count = 0;
#         for (var prop in items) {
#             if (items.hasOwnProperty(prop)) {
#                 ++count;
#             }
#         }
#         return count;
#     };

#     this.getItems = function () {
#         return items;
#     };
# }











