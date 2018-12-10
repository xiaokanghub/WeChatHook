import frida
import sys

session = frida.get_usb_device().attach(88906)
script_string = """
if (ObjC.available)
{
    try
    {
        var className = "WCDeviceStepObject";
        var funcName = "- m7StepCount";
        var hook = eval('ObjC.classes.' + className + '["' + funcName + '"]');
        console.log("[*] Class Name: " + className);
        console.log("[*] Method Name: " + funcName);
        Interceptor.attach(hook.implementation, {
          onEnter: function(args) {
            var arg0 = new ObjC.Object(args[0]);
            console.log("arg0:"+ arg0.toString());

          },
          onLeave: function(retval) {
            var retvalue = new ObjC.Object(retval);  
            console.log("retval:"+ retvalue.toString());
            newretval=ptr("0x5000");
            retval.replace(newretval);
            console.log("newretval:"+ retval);
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