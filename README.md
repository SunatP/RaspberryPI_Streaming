# RaspberryPI 4 

Specification :

```bash
CPU : Broadcom BCM2711 4-Core Cortex-A72(ARM-v8) 64-bit 1.5 GHz
RAM : 4 GB LPDDR-3200 SDRAM
GPU : OpenGL ES 3.0 
WIFI : 2.4 GHz & 5 GHz 
Audio : BCM2835 ALSA
Bluetooth : version 5.0 with BLE
LAN : Gigabit port Ethernet
Streaming Codec(Decode & Encode) : H.265 (4K60p) & H.264 (FullHD60p decode , FullHD30p encode)
Power : 5V 3A via Type-C connector also GPIO header 
```

## Setup WLAN and LAN port

We use WLAN as Access Point(**2.4 GHz**) with integrated LAN port for internet connection

first, we decided to denied interface Wireless port(**WLAN0**) by using nano to edit **dhcpcd.conf **

```bash
sudo nano /etc/dhcpcd.conf
```
then we add this line
```bash
denyinterfaces wlan0
```

next, we will set **static IP** for **WLAN port**
```bash
sudo nano /etc/network/interfaces
```
we add loopback and **eth0**(Ethernet port 0) to this file and also set static ip .
```bash
source-directory /etc/network/interfaces.d
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet static
    address 192.168.5.1
    netmask 255.255.255.0
    network 192.168.5.0
    broadcast 192.168.5.255
```
at this moment we will config the hostapd to broadcast **SSID** and **WIFI** for allow the connection then using this command.
```bash
sudo apt install hostapd
sudo nano /etc/hostapd/hostapd.conf
```
next we will add the configuration into this.
```bash
interface=wlan0 # wlan0 คือ WIFI
# driver=nl80211 # obsolete 
ssid=Name of your wish # ชื่อที่อยากจะตั้ง
hw_mode=g # จะมี 2 โหมด คือ g สำหรับ 2.4 GHz และ a สำหรับ 5 GHz
channel=6 # ช่องสัญญาณจะมีทั้งหมด 1 ถึง 14 ช่อง
ieee80211n=1 # การรับรอง แบบ 802.11n
wmm_enabled=1 # เปิดการรับรอง QoS หรือ Quality of Service
ht_capab=[HT40][SHORT-GI-20][DSSS_CCK-40] #  HT capabilities
macaddr_acl=0 # การใช้ filter สำหรับ MAC address
auth_algs=1 # 1=wpa, 2=wep, 3=both
ignore_broadcast_ssid=0
wpa=2 # ใช้แค่ WPA เท่านั้น
wpa_key_mgmt=WPA-PSK # ใช้การป้องกันความปลอดภัยแบบ WPA-PSK
wpa_passphrase=Password # รหัสอะไรก็ไดเ
rsn_pairwise=CCMP # การจับคู่แบบ CCMP 
```
After we edit **hostapd.conf** then we will go to edit **hostapd**
```bash
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo nano /etc/default/hostapd
```
find **DAEMON_CONF** and replace with
```bash
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

Next we will config dnsmasq. as I knew it dnsmasq help automatically assigned IP address for new devices connect to our network.

we must move old file of dnsmasq for backup if we config failure by using 
```bash
sudo apt install dnsmasq
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.bak
sudo nano /etc/dnsmasq.conf
```
then continue by do like this
```bash
interface=wlan0 
listen-address=192.168.5.1
bind-interfaces 
server=8.8.8.8
domain-needed
bogus-priv
dhcp-range=192.168.5.100,192.168.5.200,24h
```
after config we will reboot ther Raspberry Pi by
```bash
sudo reboot
```

## Setup Packet Forwarding 

we will config this for do the Raspberry Pi as Internet Hotspot, we can share internet from LAN(input) to WIFI(output)

we will config NAT (Network Address Translation) by
```bash
sudo nano /etc/sysctl.conf
```
then find **#net.ipv4.ip_forward=1** and remove **#** this out like this
```bash
net.ipv4.ip_forward=1
```

then do this line by line 
```bash
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE  
sudo iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
sudo iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
```
then we need to start NAT rules by applied for each start up by
```bash
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"
```
easy way is config in **etc/rc.local** by

```bash
sudo nano /etc/rc.local
```
add this **iptables-restore < /etc/iptables.ipv4.nat** and make sure correct

```bash
_IP=$(hostname -I) || true
if [ "$_IP" ]; then
    printf "My IP address is %s\n" "$_IP"
fi

iptables-restore < /etc/iptables.ipv4.nat

exit 0
```
then we will reboot again for make sure we can use Raspberry Pi to surf the internet


## Setup DLNA for streaming multimedia

after we config raspberry pi for connection, we will setup DLNA for streaming multimedia 

first install miniDLNA
```bash
sudo apt-get update && sudo apt-get install minidlna
```
after installed we will config DLNA for everyone

```bash
sudo nano /etc/minidlna.conf
```
then find **#user=minidlna** and remove **#** out
```bash
user=minidlna
```
then we will add directory path for streaming multimedia like Photo, Music and Video 

```bash
media_dir=/var/lib/minidlna
media_dir=A,/home/pi/Music # A สำหรับ Audio หรือไฟล์เสียง
media_dir=P,/home/pi/Pictures # P สำหรับ Pictures หรือไฟล์รูปภาพ
media_dir=V,/home/pi/Videos # V สำหรับ Videos หรือ ไฟล์วีดีโอ
```
after we config completed it's has 2 way to start DLNA services
```bash
sudo update-rc.d minidlna defaults
# or
sudo service minidlna start
```
after launch make sure minidlna work by type this in web browser
```bash
localhost:8200
# or 
IP address that you assigned:8200
```

we can start DLNA 3 way
```bash
sudo /etc/init.d/minidlna start
sudo /etc/init.d/minidlna stop
sudo /etc/init.d/minidlna restart
# or 
sudo service minidlna force-reload
```

## Setup Samba or SMB port for upload/download data

we must download and install samba first
```bash
sudo apt-get install samba samba-common-bin
```
then we will backup **smb.conf** for restore if config failure
```bash
sudo cp /etc/samba/smb.conf /etc/samba/smb.conf.bk
```

then we will config smaba file

```bash
sudo nano /etc/samba/smb.conf
```

we will set like this

```bash
[global]
netbios name = Pi # ชื่ออะไรก็ได้แหละ
server string = Raspberry Pi4 # ตรงนี้ตั้งไว้เหมือนอธิบายเกี่ยวกับตัวเซิร์ฟเวอร์
workgroup = WORKGROUP # ตรงนี้ไว้ใช้สำหรับ windows 
wins support = yes # Windows Internet Name Service ไม่ใช่ windows 

[HOMEPI] # ชื่อสำหรับไดรฟ์
comment=Pi shared folder # คอมเม้นท์อะไรก็ได้
path=/home/pi # ตั้งไว้ตรงไหนก็ได้ให้ user เห็นไฟล์
browseable=yes # อนุญาตให้เปลี่ยน path ได้
writeable=yes # อนุญาตให้บันทึกไฟล์หรือเขียนไฟล์ลงไดรฟ์ได้
only guest=no # อนุญาตสำหรับทุกคน
create mask=0777 # permission 0777 คือ -rwxrwxrwx

```
