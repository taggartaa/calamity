# Chris and Aaron Launch A Message Instantly To You

import calamity
import network


#connection = network.login()

app = calamity.CalamityApp()

g1 = calamity.Group("Group1")
g2 = calamity.Group("Group2")
g3 = calamity.Group("Group3")


m1 = calamity.Member(email="hello@hotmail.com", name="Bob", message="I am cooler than all you guys!")
m2 = calamity.Member(email="coolBeans@crazytown.net", name="Jamie", status="online")

m3 = calamity.Member(email="test@test.test",name="Cool Man")
m4 = calamity.Member(email="email@hotmail.com", name="Hey its working!", message="No you're not Bob!")
m5 = calamity.Member(email="whatever", name = "It has to do with the letters that are being output!")
m6 = calamity.Member(email="whatever", name = "Hmm, I wonder is this will stop at a different spot?")

m7 = calamity.Member(email="coolbeans@mytime.com", name = "Sam I Am", message="I should be in Default")

m8 = calamity.Member(email="coolbeans@mytime.com", name = "CopyCat", message="Hello There")
m9 = calamity.Member(email="coolbeanS@mytime.com", name = "CopyCat", message="Hello There")

app.add(m7)

g1.add(m1)
g1.add(m2)

g2.add(m3)
g2.add(m4)
g2.add(m5)
g2.add(m6)

g3.add(m8)
g3.add(m9)

app.add(g1)
app.add(g2)
app.add(g3)

app.run()