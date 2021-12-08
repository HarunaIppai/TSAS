import scipy.io as matlab
import numpy as np
import random
import pyqtgraph as pg

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSlider, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QSlider, QHBoxLayout
from pyqtgraph import PlotWidget, plot

# Data Initialization
data = matlab.loadmat('data.mat')
normColWb = data['y_column_normalized_wb']
maxValWb = data['y_max_wb']
normColTT = data['y_column_normalized_tt'] # Normalized Column for Weibo
maxValTT = data['y_max_tt'] # Max Value for Follower Change
minFo = 831
maxFo = 7983227
minTw = 1 # Minimum Value for tweeting
maxTw = 10000
foIntn = 50
twIntn = 10
qualInt = 10
FoInterval = []
TwInterval = []
userData = {
    "name":"",
    "platform":"", # wb or tt for Weibo or Twitter
    "follower":"", # follower count
    "point":"" # Action point a user have
}
follower = []
followerChange = [0]
post = [0]
totalPost = 0

def selectWeibo():
    userData['platform'] = 'wb'
    platformLabel.setText("Your Platform is set to Weibo")

def selectTwitter():
    userData['platform'] = 'tt'
    platformLabel.setText("Your Platform is set to Twitter")

# Function for updating the label of post count and post quality
def postCountValueUpdate():
    currentCount = postCountSlider.value()
    currentQuality = postQualitySlider.value()
    postCountLabel.setText("Your Post Amount: " + str(currentCount))
    pointConsumptionLabel.setText("The amount of point consumed: " + str(currentCount*currentQuality))
    
def postQualityValueUpdate():
    currentQuality = postQualitySlider.value()
    currentCount = postCountSlider.value()
    postQualityLabel.setText("Your Post Quality: " + str(currentQuality))
    pointConsumptionLabel.setText("The amount of point consumed: " + str(currentCount*currentQuality))

# Function For Calculating Growth
def foGrowth(platform,curFo,tweetCnt,quality): #Platform will pass the wb or tt to append Quality at a grade from 0 to 10
    for i in range(foIntn):
        if curFo < FoInterval[i]: # At the range of i-1 to i
            for j in range(twIntn):
                if tweetCnt < TwInterval[j]: # At the range of i-1 to i
                    prob = quality*random.random()*20+random.random()*80
                    k = 0
                    while prob > 0:
                        if platform == "wb":
                            prob -= normColWb[i][k][j];
                        elif platform == "tt":
                            prob -= normColTT[i][k][j];
                        k += 1
                    if platform == "wb":
                        return int(random.randint(maxValWb[i][j]*(k-1),maxValWb[i][j]*k)/198)
                    else:
                        return int(random.randint(maxValTT[i][j]*(k-1),maxValTT[i][j]*k)/25)



# Function For Calculating Follower Interval
def foInt():
    logint = (np.log10(maxFo)-np.log10(minFo))/foIntn
    for i in range(foIntn):
        FoInterval.append(10**(np.log10(minFo)+logint*i))

def twInt():
    logint = (np.log10(maxTw)-np.log10(minTw))/twIntn
    for i in range(twIntn):
        TwInterval.append(10**(np.log10(minTw)+logint*i))

def removeAllWidgetin(container):
    for widget in reversed(range(container.count())):
        if container.itemAt(widget).widget() is None:
            continue
            #removeAllWidgetin(container.itemAt(widget).layout())
        container.itemAt(widget).widget().setParent(None)

def nextDay(postCount, postQuality):
    post.append(postCount)
    #totalPost += postCount
    day = len(post)
    growth = 10
    if postCount == 0:
        growth = 0
    else:
        growth = foGrowth(userData['platform'],int(userData['follower']),postCount, postQuality/10)
    follower.append(follower[-1]+growth)
    followerChange.append(growth)
    postYesterdayCountLabel.setText("Post for yesterday: " + str(postCount))
    currentFollowerLabel.setText("Current Follower: " + str(follower[-1]))
    currentFollowerChangeLabel.setText(str(growth)+"↑")
    averageUserGrowthLabel.setText("Average User Growth: " + str(int((follower[-1]-follower[0])/(day-1))))
    dayLabel.setText("Day " + str(day) + " Of Operation")
    totalPostLabel.setText("Total post: " + str(totalPost))
    lineOfFo.setData(range(day),follower)
    lineOfFoChange.setData(range(day),followerChange)

def beginSimulation():
    global day
    day = 0
    follower.append(1000)
    userData['name'] = accountName.text()
    userData['follower'] = str(1000)
    userData['point'] = str(1000)
    print(userData)
    removeAllWidgetin(appvbox)
    #window.close()
    #windowMain = QWidget()
    window.setGeometry(600,600,500,1000)
    datavbox = QVBoxLayout()
    appvbox.addLayout(datavbox)
    channelNameLabel = QLabel(userData['name'])
    datavbox.addWidget(channelNameLabel)
    global currentFollowerLabel, currentFollowerChangeLabel, postYesterdayCountLabel, dayLabel, totalPostLabel, averageUserGrowthLabel
    hboxForFollower = QHBoxLayout()
    currentFollowerLabel = QLabel("Current Follower: " + str(follower[-1]))
    currentFollowerChangeLabel = QLabel("10↑")
    hboxForFollower.addWidget(currentFollowerLabel)
    hboxForFollower.addWidget(currentFollowerChangeLabel)
    hboxForFollower.addStretch(1)
    datavbox.addLayout(hboxForFollower)
    hboxForMiscellaneous = QHBoxLayout()
    postYesterdayCountLabel = QLabel("Post for yesterday: N/A")
    averageUserGrowthLabel = QLabel("Average User Growth: N/A")
    dayLabel = QLabel("Day " + str(day) + " Of Operation")
    totalPostLabel = QLabel("Total post: " + str(totalPost))
    vboxForPost = QVBoxLayout()
    vboxForElse = QVBoxLayout()
    vboxForPost.addWidget(postYesterdayCountLabel)
    vboxForPost.addWidget(totalPostLabel)
    vboxForElse.addWidget(dayLabel)
    vboxForElse.addWidget(averageUserGrowthLabel)
    hboxForMiscellaneous.addLayout(vboxForElse)
    hboxForMiscellaneous.addLayout(vboxForPost)
    datavbox.addLayout(hboxForMiscellaneous)
    datavbox.addLayout(postAdjustment)
    global graphWidget, lineOfFo, lineOfFoChange
    graphWidget = pg.PlotWidget()
    lineOfFo = graphWidget.plot(range(day), follower)
    graphWidget.resize(500,500)
    datavbox.addWidget(graphWidget)
    graphWidgetFoChange = pg.PlotWidget()
    lineOfFoChange = graphWidgetFoChange.plot(range(day), followerChange)
    graphWidgetFoChange.resize(500,500)
    datavbox.addWidget(graphWidgetFoChange)
    nextButton = QPushButton()
    nextButton.setText("Post and Continue")
    nextButton.clicked.connect(lambda: nextDay(postCountSlider.value(), postQualitySlider.value()))
    skipButton = QPushButton()
    skipButton.setText("Skip for next day")
    skipButton.clicked.connect(lambda: nextDay(0,0))
    datavbox.addWidget(nextButton)
    datavbox.addWidget(skipButton)
    nextDay(postCountSlider.value(), postQualitySlider.value())

def main():
    global currentQuality, currentCount
    currentCount = 1
    currentQuality = 1
    foInt()
    twInt()
    global app, window, appvbox
    app = QApplication([])
    window = QWidget()
    window.setGeometry(500,500,500,250)
    appvbox = QVBoxLayout()
    global accountName
    welcomeLabel = QLabel("Let's Create Your Virtual Account")
    accountName = QLineEdit()
    appvbox.addWidget(welcomeLabel)
    appvbox.addWidget(accountName)
    global platformLabel
    platformLabel = QLabel("Which Platform would you like it to be on:")
    buttonWeibo = QPushButton()
    buttonWeibo.setText("Weibo")
    buttonWeibo.clicked.connect(selectWeibo)
    buttonTwitter = QPushButton()
    buttonTwitter.setText("Twitter")
    buttonTwitter.clicked.connect(selectTwitter)
    appvbox.addWidget(platformLabel)
    hboxForPlatform = QHBoxLayout()
    hboxForPlatform.addWidget(buttonWeibo)
    hboxForPlatform.addWidget(buttonTwitter)
    appvbox.addLayout(hboxForPlatform)
    promptLabel = QLabel("Let's make your first tweet")
    appvbox.addWidget(promptLabel)
    global postAdjustment
    postAdjustment = QVBoxLayout()
    global postQualityLabel,postQualitySlider,postCountLabel,postCountSlider, pointConsumptionLabel
    postQualityLabel = QLabel("Your Post Quality")
    postQualitySlider = QSlider(Qt.Horizontal)
    postQualitySlider.setMinimum(1)
    postQualitySlider.setMaximum(10)
    postQualitySlider.setTickPosition(QSlider.NoTicks)
    postQualitySlider.valueChanged.connect(postQualityValueUpdate)
    postAdjustment.addWidget(postQualityLabel)
    postAdjustment.addWidget(postQualitySlider)
    postCountLabel = QLabel("Your Post Amount")
    postCountSlider = QSlider(Qt.Horizontal)
    postCountSlider.setMinimum(1)
    postCountSlider.setMaximum(100)
    postCountSlider.setTickPosition(QSlider.NoTicks)
    postCountSlider.valueChanged.connect(postCountValueUpdate)
    postAdjustment.addWidget(postCountLabel)
    postAdjustment.addWidget(postCountSlider)
    pointConsumptionLabel = QLabel("The amount of point consumed")
    postAdjustment.addWidget(pointConsumptionLabel)
    appvbox.addLayout(postAdjustment)
    beginButton = QPushButton(window)
    beginButton.setText("Let's Go")
    beginButton.clicked.connect(beginSimulation)
    appvbox.addWidget(beginButton)
    window.setLayout(appvbox)
    window.show()
    window.setWindowTitle("The Social App Simulator - Initialization")
    app.exec()
    #print(foGrowth("wb",100000,200,0.1))

if __name__ == "__main__":
    main()          



        

# print(data['y_column_normalized'][0][0][0]) # First Row: Follower Count, Second Row: Tweet Quality, Third Row: Tweet Count, Output: Interval of follower growth (from maxVal[currentFollower]*(n-1)*0.1 to maxVal*n*0.1)
# print(maxVal)