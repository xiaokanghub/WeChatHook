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
            var type = str.split(", ");
            if(type.indexOf("type=49")!=-1){
                console.log("Successful!!");
                console.log("receiver_dict:"+ receiver_dict);
                console.log("openred_dict:"+ openred_dict);

                //call function
                var WCRedEnvelopesLogicMgr = ObjC.classes.WCRedEnvelopesLogicMgr;
                var my_ReceiverQueryRedEnvelopesRequest = ObjC.chooseSync(WCRedEnvelopesLogicMgr)[0];
                my_ReceiverQueryRedEnvelopesRequest["- ReceiverQueryRedEnvelopesRequest:"](receiver_dict);
                //判断时间戳，防止封号
                if(timingIdentifier!=null){
                   console.log("OpenRed");
                   my_ReceiverQueryRedEnvelopesRequest["- OpenRedEnvelopesRequest:"](openred_dict);

                }


            }


          },
          onLeave: function(retval) {
            var string_value = ObjC.classes.NSString.stringWithString_(retval);
            console.log("Mgrretval:"+string_value+" type:"+typeof string_value);
          }
        });

        var arr;
        var url;
        var originalUrl;
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
                    var name=arr[i].substring(0,num);
                    var value=arr[i].substr(num+1);
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
           openred_dict.setObject_forKey_("https://wx.qlogo.cn/mmhead/ver_1/eDB9bF42cxyLCFib3nUjJeoWy2gibvtv1via87MAPTHEztYicBFjpiaCXEfA4BYh8cxt0dbef2o72JCaDQOPkWt2XVpmJBbjCXSib5ziavz0ssXVcY/132","headImg");
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
            console.log("timingIdentifier; ", obj.timingIdentifier);
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