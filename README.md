# InshiftBot
Shift Auto Picker for InShift  

This is a simple Python automation script using Selenium to automatically monitor and book available shifts on InShift.

The script:  
 Logs in manually (you enter your phone and OTP)  
 Monitors a specific shift page for new available jobs  
 Sends you Telegram notifications when a shift is found  
 Automatically submits the shift by clicking the "ثبت درخواست" button  



 Requirements:

- Google Chrome / ChromeDriver  
- Python packages:  
  - selenium  
  - requests  

---

## Install dependencies:

```bash
pip install selenium requests
