screen = rc.lookup("screen")

ic = ImageComparator()

if screen == "registration":
    ic.CompID = "screen1"
    ic.FileName = "C:/screens/registration.png"
    # Hide datetime &amp; mode on top panel
    ic.HiddenRegion(x1=340,x2=510,y1=0,y2=55)
    
elif screen == "login":
    ic.CompID = "screen1"
    ic.FileName = "C:/screens/login.png"
    # Hide datetime &amp; mode on top panel
    ic.HiddenRegion(x1=340,x2=510,y1=0,y2=55)
    # Hide bottom panel with hardware info
    ic.HiddenRegion(x1=10,x2=1015,y1=715,y2=768)
    
elif screen == "break":
    ic.CompID = "screen1"
    ic.FileName = "C:/screens/break.png"
    # Hide datetime &amp; mode on top panel
    ic.HiddenRegion(x1=340,x2=510,y1=0,y2=55)
    
elif screen == "logout":
    ic.CompID = "screen1"
    ic.FileName = "C:/screens/logout.png"
    # Hide datetime &amp; mode on top panel
    ic.HiddenRegion(x1=340,x2=510,y1=0,y2=55)
    
elif screen == "payment":
    ic.CompID = "screen1"
    ic.FileName = "C:/screens/payment.png"
    # Hide datetime &amp; mode on top panel
    ic.HiddenRegion(x1=340,x2=510,y1=0,y2=55)
    # Hide item in bon preview
    ic.HiddenRegion(x1=10,x2=510,y1=70,y2=460)
    # Hide title with bon sum
    ic.HiddenRegion(x1=750,x2=1030,y1=0,y2=55)

ic.Run()
