// ESP32-C6 / GDEY075T7 calendar demonstration. Hardware prototype not yet tested.
#include <Arduino.h>
#include <SPI.h>
#include <WiFi.h>
#include <Preferences.h>
#include <GxEPD2_BW.h>
#include <gdey/GxEPD2_750_GDEY075T7.h>
#include <Fonts/FreeSansBold18pt7b.h>
#include <Fonts/FreeSans12pt7b.h>
#include <time.h>
#include "config.h"

constexpr int PIN_SCK=19, PIN_MOSI=18, PIN_CS=0, PIN_DC=1, PIN_RST=2, PIN_BUSY=21;
// 800 x 80 / 8 = 8000-byte paged frame buffer.
GxEPD2_BW<GxEPD2_750_GDEY075T7,80> display(GxEPD2_750_GDEY075T7(PIN_CS,PIN_DC,PIN_RST,PIN_BUSY));
Preferences faults;
bool clockValid=false;
int shownYear=-1,shownDay=-1;

void safeHalt(const char* reason) {
  digitalWrite(PIN_CS,HIGH);
  digitalWrite(PIN_RST,LOW); // controller reset, external GDR pull-down turns Q1 off
  WiFi.mode(WIFI_OFF);
  Serial.println(reason);
  Serial.println("Panel held in reset. Inspect supply, FPC and BUSY before resetting.");
  while(true) delay(1000);
}

void busyGuard(const void*) {
  static uint32_t start=0,previous=0;
  uint32_t now=millis();
  if(!previous || now-previous>25) start=now;
  previous=now;
  // Abort before the driver's 10-second BUSY timeout. One automatic retry only.
  if(now-start>8000) {
    digitalWrite(PIN_CS,HIGH);digitalWrite(PIN_RST,LOW);
    uint8_t count=faults.getUChar("busy",0);
    faults.putUChar("busy",count+1);
    if(count==0) {
      Serial.println("BUSY timeout: controller reset, retrying once.");
      delay(100);ESP.restart();
    }
    safeHalt("BUSY timeout on retry.");
  }
  delay(1);
}

bool syncTime() {
  if(!WIFI_SSID[0]) return false;
  // Seeed's on-module RF switch: internal antenna selected, no carrier RF circuit.
  pinMode(3,OUTPUT);digitalWrite(3,LOW);
  pinMode(14,OUTPUT);digitalWrite(14,LOW);
  WiFi.mode(WIFI_STA);WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  uint32_t begin=millis();
  while(WiFi.status()!=WL_CONNECTED && millis()-begin<12000) delay(100);
  bool ok=false;
  if(WiFi.status()==WL_CONNECTED) {
    configTzTime(TZ_RULE,"pool.ntp.org","time.nist.gov");
    struct tm t;ok=getLocalTime(&t,8000) && t.tm_year>=124;
  }
  WiFi.disconnect(true);WiFi.mode(WIFI_OFF); // separate radio and refresh loads
  delay(50);
  return ok;
}

int daysInMonth(int year,int month) {
  static const int n[]={31,28,31,30,31,30,31,31,30,31,30,31};
  if(month==2 && (year%400==0 || (year%4==0 && year%100!=0))) return 29;
  return n[month-1];
}
int firstWeekday(int year,int month) { // Sunday=0; Gregorian calendar
  static const int a[]={0,3,2,5,0,3,5,1,4,6,2,4};
  if(month<3) --year;
  return (year+year/4-year/100+year/400+a[month-1]+1)%7;
}

void renderCalendar(int year,int month,int day,bool live) {
  static const char* names[]={"January","February","March","April","May","June","July","August","September","October","November","December"};
  static const char* weekdays[]={"SUN","MON","TUE","WED","THU","FRI","SAT"};
  display.setFullWindow();display.firstPage();
  do {
    display.fillScreen(GxEPD_WHITE);display.setTextColor(GxEPD_BLACK);
    display.setFont(&FreeSansBold18pt7b);display.setCursor(24,43);
    display.print(names[month-1]);display.print(" ");display.print(year);
    display.setFont(&FreeSans12pt7b);display.setCursor(24,76);
    display.print(live?"Wi-Fi synchronized calendar":"OFFLINE DEMO - fixed date");
    display.drawFastHLine(24,89,752,GxEPD_BLACK);
    const int left=24,top=134,w=107,h=48;
    for(int col=0;col<7;++col){display.setCursor(left+col*w+14,120);display.print(weekdays[col]);}
    for(int row=0;row<=6;++row) display.drawFastHLine(left,top+row*h,749,GxEPD_BLACK);
    for(int col=0;col<=7;++col) display.drawFastVLine(left+col*w,top,288,GxEPD_BLACK);
    int first=firstWeekday(year,month);
    for(int d=1;d<=daysInMonth(year,month);++d) {
      int cell=first+d-1,col=cell%7,row=cell/7;
      int x=left+col*w,y=top+row*h;
      if(d==day){display.fillRect(x+1,y+1,w-1,h-1,GxEPD_BLACK);display.setTextColor(GxEPD_WHITE);}
      display.setCursor(x+12,y+32);display.print(d);display.setTextColor(GxEPD_BLACK);
    }
    display.setCursor(24,461);display.print("EPD / C6    800 x 480    Full refresh / image retained without power");
  }while(display.nextPage());
  display.hibernate();
}

void panelTests() {
  for(int mode=0;mode<3;++mode) {
    display.setFullWindow();display.firstPage();
    do {
      display.fillScreen(mode==0?GxEPD_BLACK:GxEPD_WHITE);
      if(mode==2)for(int y=0;y<480;y+=40)for(int x=0;x<800;x+=40)
        if(((x+y)/40)%2==0)display.fillRect(x,y,40,40,GxEPD_BLACK);
    }while(display.nextPage());
    display.hibernate();delay(3000);
  }
}

void setup() {
  // Establish safe levels before configuring output drivers.
  digitalWrite(PIN_CS,HIGH);pinMode(PIN_CS,OUTPUT);
  digitalWrite(PIN_RST,LOW);pinMode(PIN_RST,OUTPUT);
  pinMode(PIN_BUSY,INPUT); // external panel actively drives BUSY
  Serial.begin(115200);delay(300);
  faults.begin("epd-c6",false);
  if(faults.getUChar("busy",0)>=2) safeHalt("Previous refresh failed twice. Clear NVS only after checking hardware.");
  clockValid=syncTime();
  SPI.begin(PIN_SCK,-1,PIN_MOSI,PIN_CS);
  display.epd2.selectSPI(SPI,SPISettings(1000000,MSBFIRST,SPI_MODE0));
  display.epd2.setBusyCallback(busyGuard);
  display.init(115200,true,10,false);
  if(RUN_PANEL_TESTS) panelTests();
  struct tm t={};
  if(clockValid) getLocalTime(&t,10);
  int y=clockValid?t.tm_year+1900:DEMO_YEAR;
  int m=clockValid?t.tm_mon+1:DEMO_MONTH;
  int d=clockValid?t.tm_mday:DEMO_DAY;
  renderCalendar(y,m,d,clockValid);
  shownYear=y;shownDay=clockValid?t.tm_yday:-1;
  faults.putUChar("busy",0);
  Serial.println("Refresh complete; panel hibernating.");
}
void loop() {
  delay(1000);
  if(!clockValid) return; // deterministic demo refreshes once per boot
  struct tm t;
  if(!getLocalTime(&t,10)) return;
  if(t.tm_year+1900==shownYear && t.tm_yday==shownDay) return;
  syncTime(); // bounded retry; existing RTC time is retained if Wi-Fi is unavailable
  getLocalTime(&t,10);
  renderCalendar(t.tm_year+1900,t.tm_mon+1,t.tm_mday,true);
  shownYear=t.tm_year+1900;shownDay=t.tm_yday;
}
